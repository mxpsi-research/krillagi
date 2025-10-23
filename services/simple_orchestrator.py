from services.agent_orchestrator_base import OrchestratorBase
from services.agent_types import ResearcherAgent, SummarizerAgent, CoderAgent, PlannerAgent
from models.agentic_db import AgenticDB
from typing import Dict, Any, List

class SimpleOrchestrator(OrchestratorBase):
    def __init__(self, session_id=None):
        super().__init__()
        self.session_id = session_id
        self.db = AgenticDB()
        # Register default agents
        self.register_agent(ResearcherAgent())
        self.register_agent(SummarizerAgent())
        self.register_agent(CoderAgent())
        self.register_agent(PlannerAgent())

    def decompose_task(self, user_prompt: str) -> List[Dict[str, Any]]:
        # Simple decomposition: assign to all agent types
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
                result = agent.execute_task(subtask["prompt"], {})
                # Record in DB (simplified)
                self.db.ensure_db()  # Ensure schema
                # In real use, insert agent, task, and analytics
                results.append({"agent": agent.name, "result": result["result"], "token_usage": result["token_usage"], "time": result["time"]})
        return results

    def aggregate_results(self, results: List[Dict[str, Any]]) -> str:
        # Simple aggregation: concatenate results
        output = "\n".join([f"[{r['agent']}] {r['result']} (Tokens: {r['token_usage']}, Time: {r['time']}s)" for r in results])
        return output
