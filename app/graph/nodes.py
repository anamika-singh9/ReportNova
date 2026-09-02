from app.graph.state import ResearchState

from app.agents.planner import PlannerAgent
from app.agents.researcher import research
from app.agents.fact_checker import FactCheckerAgent
from app.agents.report_writer import WriterAgent
from app.agents.reviewer import ReviewerAgent
from app.agents.pdf_generator import PDFGeneratorAgent
from app.agents.citation import CitationAgent

from app.utils.progress import progress


# ==================================================
# PLANNER NODE
# ==================================================

def planner_node(
    state: ResearchState,
) -> ResearchState:
    """
    Planner Agent Node.

    Creates the research plan.
    """

    progress.start_node("Planner")

    try:

        planner = PlannerAgent()

        state["plan"] = planner.plan(
            state["topic"]
        )

        progress.finish_node()

        return state

    except Exception as e:

        progress.fail_node(
            str(e)
        )

        raise


# ==================================================
# RESEARCHER NODE
# ==================================================

def researcher_node(
    state: ResearchState,
) -> ResearchState:
    """
    Research Agent Node.

    Performs web/research operations.
    """

    progress.start_node("Research")

    try:

        result = research(
            state["topic"]
        )

        state["research_data"] = (
            result["notes"]
        )

        state["sources"] = (
            result["sources"]
        )

        progress.finish_node()

        return state

    except Exception as e:

        progress.fail_node(
            str(e)
        )

        raise


# ==================================================
# FACT CHECKER NODE
# ==================================================

def fact_checker_node(
    state: ResearchState,
) -> ResearchState:
    """
    Fact Checker Agent Node.

    Verifies collected research information.
    """

    progress.start_node(
        "Fact Checker"
    )

    try:

        fact_checker = FactCheckerAgent()

        state["verified_data"] = (
            fact_checker.verify(
                state["research_data"]
            )
        )

        progress.finish_node()

        return state

    except Exception as e:

        progress.fail_node(
            str(e)
        )

        raise


# ==================================================
# WRITER NODE
# ==================================================

def writer_node(
    state: ResearchState,
) -> ResearchState:
    """
    Writer Agent Node.

    Generates the research report.
    """

    progress.start_node("Writer")

    try:

        writer = WriterAgent()

        state["report"] = writer.writer(
            state["verified_data"]
        )

        progress.finish_node()

        return state

    except Exception as e:

        progress.fail_node(
            str(e)
        )

        raise


# ==================================================
# CITATION NODE
# ==================================================

def citation_node(
    state: ResearchState,
) -> ResearchState:
    """
    Citation Agent Node.

    Adds citations according to the
    selected citation style.
    """

    progress.start_node(
        "Citation"
    )

    try:

        citation = CitationAgent()

        state["cited_report"] = (
            citation.generate(
                report=state["report"],
                sources=state["sources"],
                style=state["citation_style"],
            )
        )

        progress.finish_node()

        return state

    except Exception as e:

        progress.fail_node(
            str(e)
        )

        raise


# ==================================================
# REVIEWER NODE
# ==================================================

def reviewer_node(
    state: ResearchState,
) -> ResearchState:
    """
    Reviewer Agent Node.

    Reviews the generated report.
    """

    progress.start_node(
        "Reviewer"
    )

    try:

        reviewer = ReviewerAgent()

        state["reviewed_report"] = (
            reviewer.review(
                state["cited_report"]
            )
        )

        progress.finish_node()

        return state

    except Exception as e:

        progress.fail_node(
            str(e)
        )

        raise


# ==================================================
# PDF GENERATOR NODE
# ==================================================

def pdf_node(
    state: ResearchState,
) -> ResearchState:
    """
    PDF Generator Node.

    Generates the final PDF report.
    """

    progress.start_node(
        "PDF Generator"
    )

    try:

        pdf_generator = (
            PDFGeneratorAgent()
        )

        state["pdf_path"] = (
            pdf_generator.generate(
                state["reviewed_report"]
            )
        )

        progress.finish_node()

        return state

    except Exception as e:

        progress.fail_node(
            str(e)
        )

        raise