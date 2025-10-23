from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from models.agentic_db import AgenticDB
from services.error_handling_orchestrator import ErrorHandlingOrchestrator

app = FastAPI()

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = AgenticDB()
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str
    session_name: str = None
    topic: str = None
    model: str = None

@app.post("/chat")
async def agentic_chat(req: ChatRequest):
    # Create new session or use existing
    session_id = db.create_session(req.session_name or "Chat", req.topic)
    orchestrator = ErrorHandlingOrchestrator(session_id=session_id)
    subtasks = orchestrator.decompose_task(req.prompt)
    # Pass model to agents via context
    agent_context = {"model": req.model} if req.model else {}
    results = orchestrator.assign_tasks([
        {**subtask, "context": agent_context} for subtask in subtasks
    ])
    output = orchestrator.aggregate_results(results)
    # Log agent tasks
    import sqlite3
    for r, subtask in zip(results, subtasks):
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
    return {
        "session_id": session_id,
        "output": output,
        "results": results,
        "subtasks": subtasks
    }

@app.get("/sessions")
def get_sessions():
    sessions = db.list_sessions()
    return [{"id": s[0], "name": s[1], "topic": s[2], "created_at": s[3]} for s in sessions]

@app.get("/session/{session_id}")
def get_session(session_id: int):
    session = db.export_data(session_id)
    if not session["session"]:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.get("/session/{session_id}/history")
def get_session_history(session_id: int):
    history = db.get_session_history(session_id)
    return [{
        "prompt": h[0], "response": h[1], "model": h[2], "time_to_first_token": h[3], "total_time": h[4],
        "estimated_tokens": h[5], "total_tokens": h[6], "timestamp": h[7]
    } for h in history]

@app.post("/session/{session_id}/feedback")
def post_feedback(session_id: int, agent_id: int = None, feedback: str = ""):
    db.log_user_feedback(session_id, agent_id, feedback)
    return {"status": "ok"}

@app.get("/analytics/{session_id}")
def get_analytics(session_id: int):
    conn = db.db_path and db.db_path or "ollama_chat_perf.db"
    import sqlite3
    c = sqlite3.connect(conn).cursor()
    c.execute("SELECT metric, value, created_at FROM analytics WHERE session_id=?", (session_id,))
    rows = c.fetchall()
    return [{"metric": r[0], "value": r[1], "created_at": r[2]} for r in rows]

@app.get("/agents")
def get_agents():
    conn = db.db_path and db.db_path or "ollama_chat_perf.db"
    import sqlite3
    c = sqlite3.connect(conn).cursor()
    c.execute("SELECT id, name, type, description, created_at FROM agents")
    rows = c.fetchall()
    return [{"id": r[0], "name": r[1], "type": r[2], "description": r[3], "created_at": r[4]} for r in rows]
