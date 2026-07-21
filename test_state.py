from app.graph.state import ResearchState
from app.graph.nodes import planner_node

state: ResearchState = {
    "topic": "Artificial Intelligence",
    "plan": None,
    "research_data": None,
    "verified_data": None,
    "report": None,
    "reviewed_report": None,
    "pdf_path": None
}

result = planner_node(state)

print(result["plan"])