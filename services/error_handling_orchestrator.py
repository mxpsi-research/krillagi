from services.agent_orchestrator_base import OrchestratorBase
from services.agent_types import ResearcherAgent, SummarizerAgent, CoderAgent, PlannerAgent
from models.agentic_db import AgenticDB
from typing import Dict, Any, List
import time

class ErrorHandlingOrchestrator(OrchestratorBase):
    def __init__(self, session_id=None, max_retries=2):
        super().__init__()
        self.session_id = session_id
        self.db = AgenticDB()
        self.max_retries = max_retries
        self.register_agent(ResearcherAgent())
        self.register_agent(SummarizerAgent())
        self.register_agent(CoderAgent())
        self.register_agent(PlannerAgent())

    def decompose_task(self, user_prompt: str) -> List[Dict[str, Any]]:
        return [
            {"agent_type": "researcher", "prompt": user_prompt},
            {"agent_type": "summarizer", "prompt": user_prompt},
            {"agent_type": "coder", "prompt": user_prompt},
            {"agent_type": "planner", "prompt": user_prompt}
        ]

    def assign_tasks(self, subtasks: List[Dict[str, Any]]):
        results = []
        for subtask in subtasks:
            agent = next((a for a in self.agents if a.agent_type == subtask["agent_type"]), None)
            if agent:
                attempt = 0
                while attempt <= self.max_retries:
                    try:
                        start = time.time()
                        result = agent.execute_task(subtask["prompt"], {})
                        elapsed = time.time() - start
                        # Simulate error for demonstration
                        if subtask["agent_type"] == "coder" and attempt < self.max_retries:
                            raise Exception("Simulated agent failure")
                        results.append({
                            "agent": agent.name,
                            "result": result["result"],
                            "token_usage": result["token_usage"],
                            "time": elapsed,
                            "attempts": attempt + 1
                        })
                        break
                    except Exception as e:
                        self.db.ensure_db()
                        self.db.ensure_db() # Ensure schema
                        # Log error in orchestrator_events
                        conn = self.db.db_path and self.db.db_path or "ollama_chat_perf.db"
                        dbconn = AgenticDB(conn)
                        # Insert error event (simplified)
                        # In real use, add a method to AgenticDB for this
                        print(f"Error in agent '{agent.name}' (attempt {attempt+1}): {e}")
                        attempt += 1
                        if attempt > self.max_retries:
                            print(f"Agent '{agent.name}' failed after {self.max_retries} retries.")
        return results

    def aggregate_results(self, results: List[Dict[str, Any]]) -> str:
        output = "\n".join([f"[{r['agent']}] {r['result']} (Tokens: {r['token_usage']}, Time: {r['time']:.2f}s, Attempts: {r['attempts']})" for r in results])
        return output
