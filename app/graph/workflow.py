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

from app.graph.router import (
    research_router,
    fact_check_router,
)


# ==================================================
# WORKFLOW NODES
# ==================================================

WORKFLOW_NODES = [
    "planner",
    "researcher",
    "fact_checker",
    "writer",
    "citation",
    "reviewer",
    "pdf_generator",
]


# ==================================================
# BUILD GRAPH
# ==================================================

def build_graph():
    """
    Build and compile the LangGraph research workflow.

    Workflow:

        Planner
           ↓
        Researcher
           ↓
        Fact Checker
           ↓
        Writer
           ↓
        Citation
           ↓
        Reviewer
           ↓
        PDF Generator
           ↓
          END

    Researcher and Fact Checker can terminate
    the workflow through their respective routers.
    """

    workflow = StateGraph(
        ResearchState
    )

    # --------------------------------------------------
    # Add Nodes
    # --------------------------------------------------

    workflow.add_node(
        "planner",
        planner_node,
    )

    workflow.add_node(
        "researcher",
        researcher_node,
    )

    workflow.add_node(
        "fact_checker",
        fact_checker_node,
    )

    workflow.add_node(
        "writer",
        writer_node,
    )

    workflow.add_node(
        "citation",
        citation_node,
    )

    workflow.add_node(
        "reviewer",
        reviewer_node,
    )

    workflow.add_node(
        "pdf_generator",
        pdf_node,
    )

    # --------------------------------------------------
    # Entry Point
    # --------------------------------------------------

    workflow.set_entry_point(
        "planner"
    )

    # --------------------------------------------------
    # Planner → Researcher
    # --------------------------------------------------

    workflow.add_edge(
        "planner",
        "researcher",
    )

    # --------------------------------------------------
    # Researcher → Conditional Router
    # --------------------------------------------------

    workflow.add_conditional_edges(

        "researcher",

        research_router,

        {
            "continue": "fact_checker",
            "stop": END,
        },

    )

    # --------------------------------------------------
    # Fact Checker → Conditional Router
    # --------------------------------------------------

    workflow.add_conditional_edges(

        "fact_checker",

        fact_check_router,

        {
            "continue": "writer",
            "stop": END,
        },

    )

    # --------------------------------------------------
    # Writer → Citation
    # --------------------------------------------------

    workflow.add_edge(
        "writer",
        "citation",
    )

    # --------------------------------------------------
    # Citation → Reviewer
    # --------------------------------------------------

    workflow.add_edge(
        "citation",
        "reviewer",
    )

    # --------------------------------------------------
    # Reviewer → PDF Generator
    # --------------------------------------------------

    workflow.add_edge(
        "reviewer",
        "pdf_generator",
    )

    # --------------------------------------------------
    # PDF Generator → END
    # --------------------------------------------------

    workflow.add_edge(
        "pdf_generator",
        END,
    )

    # --------------------------------------------------
    # Compile
    # --------------------------------------------------

    return workflow.compile()


# ==================================================
# TOTAL WORKFLOW NODES
# ==================================================

def total_workflow_nodes() -> int:
    """
    Return the number of executable agent nodes.

    This value is used by ProgressTracker to calculate
    workflow completion percentage.
    """

    return len(WORKFLOW_NODES)

