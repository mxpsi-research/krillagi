import sqlite3

DB_PATH = "ollama_chat_perf.db"

class ChatPerfDB:
    def get_session_history(self, session_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            SELECT prompt, response, model, time_to_first_token, total_time, estimated_tokens, total_tokens, timestamp
            FROM chat_perf WHERE session_id = ? ORDER BY timestamp ASC
        """, (session_id,))
        history = c.fetchall()
        conn.close()
        return history

    def delete_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Delete chat history for session
        c.execute("DELETE FROM chat_perf WHERE session_id = ?", (session_id,))
        # Delete session itself
        c.execute("DELETE FROM chat_sessions WHERE id = ?", (session_id,))
        conn.commit()
        conn.close()
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.ensure_db()

    def ensure_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Create chat_sessions table
        c.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                topic TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Create chat_perf table with session_id foreign key
        c.execute("""
            CREATE TABLE IF NOT EXISTS chat_perf (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                prompt TEXT,
                response TEXT,
                model TEXT,
                time_to_first_token REAL,
                total_time REAL,
                estimated_tokens INTEGER,
                total_tokens INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES chat_sessions(id)
            )
        """)
        conn.commit()
        conn.close()

    def create_session(self, name, topic=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO chat_sessions (name, topic) VALUES (?, ?)
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

    def save_perf(self, session_id, prompt, response, model, time_to_first, total_time, est_tokens, total_tokens):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO chat_perf (session_id, prompt, response, model, time_to_first_token, total_time, estimated_tokens, total_tokens)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (session_id, prompt, response, model, time_to_first, total_time, est_tokens, total_tokens))
        conn.commit()
        conn.close()
