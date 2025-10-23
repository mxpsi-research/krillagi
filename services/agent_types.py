from services.agent_orchestrator_base import AgentBase
from typing import Dict, Any

class ResearcherAgent(AgentBase):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Researcher prefers to work first, no dependencies
        return {"mode": "sequential", "depends_on": []}
    def __init__(self, agent_id=None):
        super().__init__(agent_id, name="Researcher", agent_type="researcher", description="Finds and gathers information relevant to the task.")
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder: In real use, call LLM or external API
        return {"result": f"Research findings for: {prompt}", "token_usage": 10, "time": 1.0}

class SummarizerAgent(AgentBase):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Summarizer prefers to work after researcher
        return {"mode": "sequential", "depends_on": ["researcher"]}
    def __init__(self, agent_id=None):
        super().__init__(agent_id, name="Summarizer", agent_type="summarizer", description="Summarizes information and results.")
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"result": f"Summary of: {prompt}", "token_usage": 5, "time": 0.5}

class CoderAgent(AgentBase):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Coder can work after researcher and/or planner
        return {"mode": "sequential", "depends_on": ["researcher", "planner"]}
    def __init__(self, agent_id=None):
        super().__init__(agent_id, name="Coder", agent_type="coder", description="Writes code or scripts to solve problems.")
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"result": f"Code for: {prompt}", "token_usage": 20, "time": 2.0}

class PlannerAgent(AgentBase):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Planner can work after researcher
        return {"mode": "sequential", "depends_on": ["researcher"]}
    def __init__(self, agent_id=None):
        super().__init__(agent_id, name="Planner", agent_type="planner", description="Plans and organizes steps to complete tasks.")
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"result": f"Plan for: {prompt}", "token_usage": 8, "time": 1.2}
