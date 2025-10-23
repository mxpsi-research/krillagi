from services.simple_orchestrator import SimpleOrchestrator

def test_agent_collaboration(user_prompt):
    orchestrator = SimpleOrchestrator()
    subtasks = orchestrator.decompose_task(user_prompt)
    # Gather agent self-assessment
    agent_prefs = {}
    for subtask in subtasks:
        agent = next((a for a in orchestrator.agents if a.agent_type == subtask["agent_type"]), None)
        if agent:
            agent_prefs[agent.agent_type] = agent.preferred_collaboration(subtask["prompt"], {})
    print("Agent collaboration preferences:")
    for agent_type, pref in agent_prefs.items():
        print(f"- {agent_type}: mode={pref['mode']}, depends_on={pref['depends_on']}")
    # Simulate sequential collaboration based on dependencies
    context = {}
    results = []
    for subtask in subtasks:
        agent = next((a for a in orchestrator.agents if a.agent_type == subtask["agent_type"]), None)
        if agent:
            # Wait for dependencies
            deps = agent_prefs[agent.agent_type]["depends_on"]
            for dep in deps:
                dep_result = next((r for r in results if r["agent_type"] == dep), None)
                if dep_result:
                    context[dep] = dep_result["result"]
            result = agent.execute_task(subtask["prompt"], context)
            results.append({"agent_type": agent.agent_type, "result": result["result"]})
    print("\nCollaboration results:")
    for r in results:
        print(f"[{r['agent_type']}] {r['result']}")

if __name__ == "__main__":
    test_agent_collaboration("How can I build a solar-powered robot?")
