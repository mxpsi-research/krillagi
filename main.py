

# Use agentic workflow
from models.agentic_db import AgenticDB
from services.error_handling_orchestrator import ErrorHandlingOrchestrator
from services.ollama_service import is_ollama_installed, is_ollama_running, get_installed_models
from utils.ollama_utils import OLLAMA_API_URL, OLLAMA_CLOUD_DEFAULT_MODEL, prompt_model_choice
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

    db = AgenticDB()
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
    orchestrator = ErrorHandlingOrchestrator(session_id=session_id)
    while True:
        prompt = input("You: ")
        if prompt.strip().lower() == "exit":
            break
        # Agentic workflow: decompose, assign, aggregate
        subtasks = orchestrator.decompose_task(prompt)
        results = orchestrator.assign_tasks(subtasks)
        output = orchestrator.aggregate_results(results)
        print("\nAgentic Workflow Results:")
        print(output)
        # Log agent tasks in DB
        for r, subtask in zip(results, subtasks):
            # Find agent_id (not implemented, so use None)
            db.ensure_db()
            conn = sqlite3.connect(db.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO agent_tasks (agent_id, session_id, status, prompt, response, token_usage, time_to_first_token, total_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (None, session_id, "completed", subtask["prompt"], r["result"], r["token_usage"], None, r["time"]))
            conn.commit()
            conn.close()
        # Log analytics
        for r in results:
            db.log_analytics(session_id, None, "token_usage", r["token_usage"])
            db.log_analytics(session_id, None, "time", r["time"])
            db.log_analytics(session_id, None, "attempts", r.get("attempts", 1))
        # User feedback
        feedback = input("\nReview the results above. Enter feedback or 'approve': ")
        db.log_user_feedback(session_id, None, feedback)
        print("Feedback recorded.")

if __name__ == "__main__":
    main()
