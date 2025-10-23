# Agentic schema for krillAGI
# This module defines the database models for agents, agent tasks, orchestrator events, analytics, and session/task history.

import sqlite3

DB_PATH = "ollama_chat_perf.db"

class AgenticDB:
    def create_session(self, name, topic=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO chat_sessions (name, topic, created_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (name, topic))
        session_id = c.lastrowid
        conn.commit()
        conn.close()
        return session_id
    def list_sessions(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, name, topic, created_at FROM chat_sessions ORDER BY created_at DESC")
        sessions = c.fetchall()
        conn.close()
        return sessions
    def log_sensitive_action(self, session_id, agent_id, action, details):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO orchestrator_events (session_id, event_type, details)
            VALUES (?, ?, ?)
        """, (session_id, action, details))
        conn.commit()
        conn.close()

    def export_data(self, session_id, redact_sensitive=False):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Export chat, agent tasks, analytics
        c.execute("SELECT * FROM chat_sessions WHERE id=?", (session_id,))
        session = c.fetchone()
        c.execute("SELECT * FROM agent_tasks WHERE session_id=?", (session_id,))
        tasks = c.fetchall()
        c.execute("SELECT * FROM analytics WHERE session_id=?", (session_id,))
        analytics = c.fetchall()
        if redact_sensitive:
            # Redact sensitive fields (example: response)
            tasks = [(t[0], t[1], t[2], t[3], t[4], t[5], "[REDACTED]", t[7], t[8], t[9], t[10], t[11], t[12]) for t in tasks]
        conn.close()
        return {"session": session, "tasks": tasks, "analytics": analytics}
    def log_analytics(self, session_id, agent_id, metric, value):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO analytics (session_id, agent_id, metric, value)
            VALUES (?, ?, ?, ?)
        """, (session_id, agent_id, metric, value))
        conn.commit()
        conn.close()

    def log_user_feedback(self, session_id, agent_id, feedback):
        self.log_analytics(session_id, agent_id, "user_feedback", feedback)
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.ensure_db()

    def ensure_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Agents table
        c.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Agent tasks table
        c.execute("""
            CREATE TABLE IF NOT EXISTS agent_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id INTEGER,
                session_id INTEGER,
                parent_task_id INTEGER,
                status TEXT,
                prompt TEXT,
                response TEXT,
                token_usage INTEGER,
                time_to_first_token REAL,
                total_time REAL,
                completed_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(agent_id) REFERENCES agents(id),
                FOREIGN KEY(session_id) REFERENCES chat_sessions(id),
                FOREIGN KEY(parent_task_id) REFERENCES agent_tasks(id)
            )
        """)
        # Orchestrator events table
        c.execute("""
            CREATE TABLE IF NOT EXISTS orchestrator_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                event_type TEXT,
                details TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES chat_sessions(id)
            )
        """)
        # Analytics table
        c.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                agent_id INTEGER,
                metric TEXT,
                value REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES chat_sessions(id),
                FOREIGN KEY(agent_id) REFERENCES agents(id)
            )
        """)
        conn.commit()
        conn.close()

    def get_session_history(self, session_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            SELECT prompt, response, time_to_first_token, total_time, token_usage, created_at
            FROM agent_tasks WHERE session_id = ? ORDER BY created_at ASC
        """, (session_id,))
        history = c.fetchall()
        conn.close()
        return history
