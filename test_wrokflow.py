from app.graph.workflow import build_graph

graph = build_graph()

state = {
    "topic": "Artificial Intelligence",
    "plan": None,
    "research_data": None,
    "verified_data": None,
    "report": None,
    "reviewed_report": None,
    "pdf_path": None,
}

result = graph.invoke(state)

print("\nWorkflow Completed!\n")
print(result["pdf_path"])