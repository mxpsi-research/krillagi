from services.agent_orchestrator_base import AgentBase
from typing import Dict, Any

import requests
from utils.ollama_utils import OLLAMA_API_URL

class ResearcherAgent(AgentBase):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"mode": "sequential", "depends_on": []}
    def __init__(self, agent_id=None):
        super().__init__(agent_id, name="Researcher", agent_type="researcher", description="Finds and gathers information relevant to the task.")
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        model = context.get("model") or "llama2"
        try:
            res = requests.post(f"{OLLAMA_API_URL}/api/generate", json={"model": model, "prompt": prompt})
            if res.ok:
                data = res.json()
                return {"result": data.get("response", ""), "token_usage": data.get("eval_count", 0), "time": data.get("total_duration", 0)/1000.0}
        except Exception as e:
            return {"result": f"[Ollama error: {e}]", "token_usage": 0, "time": 0.0}
        return {"result": f"Research findings for: {prompt}", "token_usage": 10, "time": 1.0}

class SummarizerAgent(AgentBase):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"mode": "sequential", "depends_on": ["researcher"]}
    def __init__(self, agent_id=None):
        super().__init__(agent_id, name="Summarizer", agent_type="summarizer", description="Summarizes information and results.")
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        model = context.get("model") or "llama2"
        try:
            res = requests.post(f"{OLLAMA_API_URL}/api/generate", json={"model": model, "prompt": prompt})
            if res.ok:
                data = res.json()
                return {"result": data.get("response", ""), "token_usage": data.get("eval_count", 0), "time": data.get("total_duration", 0)/1000.0}
        except Exception as e:
            return {"result": f"[Ollama error: {e}]", "token_usage": 0, "time": 0.0}
        return {"result": f"Summary of: {prompt}", "token_usage": 5, "time": 0.5}

class CoderAgent(AgentBase):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"mode": "sequential", "depends_on": ["researcher", "planner"]}
    def __init__(self, agent_id=None):
        super().__init__(agent_id, name="Coder", agent_type="coder", description="Writes code or scripts to solve problems.")
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        model = context.get("model") or "llama2"
        try:
            res = requests.post(f"{OLLAMA_API_URL}/api/generate", json={"model": model, "prompt": prompt})
            if res.ok:
                data = res.json()
                return {"result": data.get("response", ""), "token_usage": data.get("eval_count", 0), "time": data.get("total_duration", 0)/1000.0}
        except Exception as e:
            return {"result": f"[Ollama error: {e}]", "token_usage": 0, "time": 0.0}
        return {"result": f"Code for: {prompt}", "token_usage": 20, "time": 2.0}

class PlannerAgent(AgentBase):
    def preferred_collaboration(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"mode": "sequential", "depends_on": ["researcher"]}
    def __init__(self, agent_id=None):
        super().__init__(agent_id, name="Planner", agent_type="planner", description="Plans and organizes steps to complete tasks.")
    def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        model = context.get("model") or "llama2"
        try:
            res = requests.post(f"{OLLAMA_API_URL}/api/generate", json={"model": model, "prompt": prompt})
            if res.ok:
                data = res.json()
                return {"result": data.get("response", ""), "token_usage": data.get("eval_count", 0), "time": data.get("total_duration", 0)/1000.0}
        except Exception as e:
            return {"result": f"[Ollama error: {e}]", "token_usage": 0, "time": 0.0}
        return {"result": f"Plan for: {prompt}", "token_usage": 8, "time": 1.2}
