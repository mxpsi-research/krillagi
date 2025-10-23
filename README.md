
# 🦐 krillAGI

krillAGI is a full-stack agentic orchestration platform for LLM-powered workflows, featuring a Python FastAPI backend, Next.js/Tailwind frontend dashboard, agentic collaboration, analytics, and visualization.

## Features
- Agentic workflow orchestration (Python backend)
- Multiple agent types (researcher, summarizer, coder, planner)
- SQLite3 database for chat, agent tasks, analytics, and session history
- FastAPI REST API for frontend/backend integration
- Next.js/Tailwind dashboard with:
  - Chat UI (with session history, deletion)
  - Agentic task flow graph (Cytoscape.js)
  - Agent data and analytics (live updates)
  - Light mode, two-column layout
- Error handling, extensibility, and security features

## Requirements
- Python 3.9+
- Node.js 18+
- [Ollama](https://ollama.com/download) installed and running (for LLM chat)
- Python packages: `requests`, `sqlite3`, `fastapi`, `uvicorn`
- Node packages: `next`, `react`, `tailwindcss`, `cytoscape`, etc.

## Usage

### Backend (FastAPI)
1. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```

### Frontend (Next.js)
1. Install Node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start frontend dev server:
   ```bash
   npm run dev
   ```
3. Open [http://localhost:3000](http://localhost:3000)

## Data & Troubleshooting
- All data is stored in `ollama_chat_perf.db` (excluded by `.gitignore`).
- If you see errors about Ollama not responding:
  - Make sure Ollama is running (`ollama serve`)
  - Ensure your model is available (`ollama pull <model>`)
  - Check that Ollama is reachable at `http://localhost:11434`
  - Review error messages for specific guidance

## License
MIT
