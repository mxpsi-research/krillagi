from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class AgentBase(ABC):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agents can declare their preferred collaboration mode and dependencies for a given task.
        Returns a dict, e.g. {"mode": "sequential", "depends_on": ["researcher"]}
        Default: no preference.
        """
        return {"mode": None, "depends_on": []}
    def __init__(self, agent_id: Optional[int] = None, name: str = "", agent_type: str = "generic", description: str = ""):
        self.agent_id = agent_id
        self.name = name
        self.agent_type = agent_type
        self.description = description

    @abstractmethod
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent on a given prompt and context, return result and analytics."""
        pass

    def can_handle(self, task_type: str) -> bool:
        """Return True if agent can handle the given task type."""
        return True

class OrchestratorBase(ABC):
    def __init__(self):
        self.agents: List[AgentBase] = []
        self.session_id: Optional[int] = None
        self.analytics: List[Dict[str, Any]] = []

    def register_agent(self, agent: AgentBase):
        self.agents.append(agent)

    @abstractmethod
    def decompose_task(self, user_prompt: str) -> List[Dict[str, Any]]:
        """Break down user prompt into subtasks for agents."""
        pass

    @abstractmethod
    def assign_tasks(self, subtasks: List[Dict[str, Any]]):
        """Assign subtasks to agents and monitor execution."""
        pass

    @abstractmethod
    def aggregate_results(self, results: List[Dict[str, Any]]) -> Any:
        """Aggregate results from agents into a final output."""
        pass

    def monitor_agents(self):
        """Monitor agent status, token usage, timing, and prompt user for clarification if needed."""
        pass

    def is_solution_complete(self, results: List[Dict[str, Any]]) -> bool:
        """Determine if the solution is complete based on agent outputs and user feedback."""
        return True
