from services.error_handling_orchestrator import ErrorHandlingOrchestrator
from models.agentic_db import AgenticDB

def run_agentic_workflow_with_feedback(user_prompt, session_id=1):
    orchestrator = ErrorHandlingOrchestrator(session_id=session_id)
    subtasks = orchestrator.decompose_task(user_prompt)
    results = orchestrator.assign_tasks(subtasks)
    output = orchestrator.aggregate_results(results)
    print("\nAgentic Workflow Results:")
    print(output)
    # Track analytics
    db = AgenticDB()
    for r in results:
        # In real use, agent_id would be looked up
        db.log_analytics(session_id, None, "token_usage", r["token_usage"])
        db.log_analytics(session_id, None, "time", r["time"])
        db.log_analytics(session_id, None, "attempts", r["attempts"])
    # User feedback
    feedback = input("\nReview the results above. Enter feedback or 'approve': ")
    db.log_user_feedback(session_id, None, feedback)
    print("Feedback recorded.")

if __name__ == "__main__":
    run_agentic_workflow_with_feedback("How can I build a solar-powered robot?")
