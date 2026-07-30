from langgraph.graph import StateGraph, END

from app.graph.state import ResearchState
from app.graph.nodes import (
    planner_node,
    researcher_node,
    fact_checker_node,
    writer_node,
    citation_node,
    reviewer_node,
    pdf_node,
)

from app.graph.router import(
    research_router,
    fact_check_router
)


def build_graph():
    """
    Build and compile the LangGraph workflow.
    """

    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("fact_checker", fact_checker_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("citation", citation_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("pdf_generator", pdf_node)

    # Set entry point
    workflow.set_entry_point("planner")

    # Connect nodes
    workflow.add_edge("planner", "researcher")
    
    workflow.add_conditional_edges(
    "researcher",
    research_router,
    {
        "continue": "fact_checker",
        "stop": END,
    },
    )

    workflow.add_conditional_edges(
    "fact_checker",
    fact_check_router,
    {
        "continue": "writer",
        "stop": END,
    },
    )

    workflow.add_edge("writer", "citation")
    workflow.add_edge("citation", "reviewer")
    workflow.add_edge("reviewer", "pdf_generator")

    # Finish workflow
    workflow.add_edge("pdf_generator", END)

    return workflow.compile()

def total_workflow_nodes():
    """
    Returns total executable nodes.
    """

    graph = build_graph()

    return len(graph.get_graph().nodes) - 2