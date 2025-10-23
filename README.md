# krillAGI

krillAGI is a Python-based CLI tool for running chat sessions with Ollama LLM models and logging performance metrics to SQLite3. It includes robust error handling and user guidance for troubleshooting Ollama connectivity and model issues.

## Features
* Checks if Ollama is installed and running
* Lists available Ollama models and prompts for selection (defaults to `gtp-oss:20b-cloud`)
* Runs chat sessions with selected model
* Logs chat history and LLM performance data to SQLite3, including:
   - Time to first token/character
   - Estimated token usage
   - Total tokens after each prompt
* Provides clear error messages and troubleshooting steps if Ollama is not running, unreachable, or if the model is missing

## Requirements
- Python 3.9+
- [Ollama](https://ollama.com/download) installed and running
- Python packages: `requests`, `sqlite3` (standard library)

## Usage
1. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start Ollama server:
   ```bash
   ollama serve
   ```
3. (Optional) Pull a model, e.g.:
   ```bash
   ollama pull gtp-oss:20b-cloud
   ```
4. Run krillAGI:
   ```bash
   python main.py
   ```

## Data
## Data & Troubleshooting
- Chat and performance logs are saved in `ollama_chat_perf.db` (excluded by `.gitignore`).
- If you see errors about Ollama not responding:
   - Make sure Ollama is running (`ollama serve`)
   - Ensure your model is available (`ollama pull <model>`)
   - Check that Ollama is reachable at `http://localhost:11434`
   - Review error messages for specific guidance

## License
MIT
