import subprocess
import requests
from utils.ollama_utils import OLLAMA_API_URL

def is_ollama_installed():
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def is_ollama_running():
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except Exception:
        return False

def get_installed_models():
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        if response.status_code == 200:
            data = response.json()
            return [m['name'] for m in data.get('models', [])]
        return []
    except Exception:
        return []
