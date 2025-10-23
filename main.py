
from models.chat_perf_db import ChatPerfDB
from services.ollama_service import is_ollama_installed, is_ollama_running, get_installed_models
from utils.ollama_utils import OLLAMA_API_URL, OLLAMA_CLOUD_DEFAULT_MODEL, prompt_model_choice
from utils.token_utils import estimate_tokens
import sys
import time
import json
import requests

def main():
    if not is_ollama_installed():
        print("Ollama is not installed. Please install from https://ollama.com/download and try again.")
        sys.exit(1)
    if not is_ollama_running():
        print("Ollama is not running. Please start Ollama (usually 'ollama serve') and try again.")
        sys.exit(1)

    db = ChatPerfDB()
    models = get_installed_models()
    model = prompt_model_choice(models) if models else OLLAMA_CLOUD_DEFAULT_MODEL
    print(f"Using model: {model}")

    # Ask user for preferred output format/structure
    print("\nHow would you like chat history and performance data to be formatted for output?")
    print("1. Table (default)")
    print("2. CSV")
    print("3. JSON")
    output_format = input("Choose format [1-3]: ").strip()
    if output_format not in ['2', '3']:
        output_format = '1'

    # Session selection/creation
    sessions = db.list_sessions()
    print("\nAvailable chat sessions:")
    for s in sessions:
        print(f"{s[0]}. {s[1]} (topic: {s[2] or 'N/A'}, created: {s[3]})")
    print("N. Start a new chat session")
    print("H. View session history")
    print("D. Delete a session")

    session_id = None
    while session_id is None:
        session_choice = input("Select session by number, 'N' for new, 'H' for history, 'D' for delete: ").strip()
        if session_choice.lower() == 'n' or (session_choice.isdigit() and int(session_choice) not in [s[0] for s in sessions]):
            name = input("Enter a name for this chat session: ").strip()
            topic = input("Enter a topic (optional): ").strip()
            session_id = db.create_session(name, topic if topic else None)
            print(f"Created new session '{name}' (id: {session_id})")
        elif session_choice.lower() == 'h':
            sid = input("Enter session number to view history: ").strip()
            if sid.isdigit() and int(sid) in [s[0] for s in sessions]:
                history = db.get_session_history(int(sid))
                print(f"\nHistory for session {sid}:")
                for idx, h in enumerate(history, 1):
                    print(f"[{idx}] {h[7]}\nPrompt: {h[0]}\nResponse: {h[1]}\nModel: {h[2]}\nFirst token: {h[3]:.3f}s, Total: {h[4]:.3f}s, Prompt tokens: {h[5]}, Response tokens: {h[6]}\n")
            else:
                print("Invalid session number.")
        elif session_choice.lower() == 'd':
            sid = input("Enter session number to delete: ").strip()
            if sid.isdigit() and int(sid) in [s[0] for s in sessions]:
                confirm = input(f"Are you sure you want to delete session {sid}? This will remove all chat history. (y/N): ").strip().lower()
                if confirm == 'y':
                    db.delete_session(int(sid))
                    print(f"Session {sid} deleted.")
                    sessions = db.list_sessions()
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid session number.")
        elif session_choice.isdigit() and int(session_choice) in [s[0] for s in sessions]:
            session_id = int(session_choice)
            print(f"Continuing session '{[s[1] for s in sessions if s[0]==session_id][0]}' (id: {session_id})")
        else:
            print("Invalid choice.")

    print("Type 'exit' to quit.")
    while True:
        prompt = input("You: ")
        if prompt.strip().lower() == "exit":
            break
        payload = {"model": model, "prompt": prompt}
        start_time = time.time()
        first_token_time = None
        response_text = ""
        total_tokens = 0
        try:
            with requests.post(f"{OLLAMA_API_URL}/api/generate", json=payload, stream=True, timeout=30) as r:
                if r.status_code != 200:
                    print(f"Error: Ollama did not respond (HTTP {r.status_code}). Is Ollama running and is the model available?")
                    print("Try running 'ollama serve' and ensure your model is pulled with 'ollama pull <model>'.")
                    continue
                got_response = False
                for chunk in r.iter_lines():
                    if chunk:
                        data = json.loads(chunk.decode())
                        token = data.get("response", "")
                        if token:
                            got_response = True
                            if first_token_time is None:
                                first_token_time = time.time() - start_time
                            response_text += token
                            total_tokens += estimate_tokens(token)
                        if data.get("done"):
                            break
                if not got_response:
                    print("No response received from Ollama. Check if the model is available and try again.")
                    continue
            total_time = time.time() - start_time
            est_tokens = estimate_tokens(prompt)
            db.save_perf(session_id, prompt, response_text, model, first_token_time or 0, total_time, est_tokens, total_tokens)
            print(f"Ollama: {response_text}")
            first_token_time_fmt = first_token_time if first_token_time is not None else 0.0
            print(f"Perf: First token: {first_token_time_fmt:.3f}s, Total: {total_time:.3f}s, Prompt tokens: {est_tokens}, Response tokens: {total_tokens}")
        except requests.exceptions.Timeout:
            print("Error: Request to Ollama timed out. Is Ollama running and reachable at http://localhost:11434?")
        except Exception as e:
            print(f"Error during chat: {e}")

if __name__ == "__main__":
    main()
