# krillAGI Backend

This is the FastAPI backend for krillAGI, providing agentic orchestration, analytics, and REST API endpoints for the frontend dashboard.

## Features
- Agentic workflow orchestration (multiple agent types)
- SQLite3 database for chat, agent tasks, analytics, and session history
- REST API endpoints for sessions, agents, analytics, feedback, and visualization
- Error handling, extensibility, and security features

## Setup
1. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```

## API Endpoints
- `/sessions` - List chat sessions
- `/session/{session_id}` - Get session data
- `/session/{session_id}/history` - Get chat/agent history
- `/session/{session_id}/feedback` - Post user feedback
- `/analytics/{session_id}` - Get analytics for session
- `/agents` - List agents

## Data
- All data is stored in `ollama_chat_perf.db` (excluded by `.gitignore`).

## Troubleshooting
- If you see errors about Ollama not responding:
  - Make sure Ollama is running (`ollama serve`)
  - Ensure your model is available (`ollama pull <model>`)
  - Check that Ollama is reachable at `http://localhost:11434`

## License
MIT
