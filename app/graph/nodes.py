from app.graph.state import ResearchState
from app.agents.planner import PlannerAgent
from app.agents.researcher import research
from app.agents.fact_checker import FactCheckerAgent
from app.agents.report_writer import WriterAgent
from app.agents.reviewer import ReviewerAgent
from app.agents.pdf_generator import PDFGeneratorAgent
from app.agents.citation import CitationAgent
from app.utils.progress import progress


def planner_node(state: ResearchState) -> ResearchState:
    """Planner Node"""

    progress.start_node("Planner")

    try:
        planner = PlannerAgent()

        state["plan"] = planner.plan(
            state["topic"]
        )

        return state

    finally:
        progress.finish_node()


def researcher_node(state: ResearchState) -> ResearchState:
    """Researcher Node"""

    progress.start_node("Research")

    try:
        result = research(state["topic"])

        state["research_data"] = result["notes"]
        state["sources"] = result["sources"]

        return state

    finally:
        progress.finish_node()


def fact_checker_node(state: ResearchState) -> ResearchState:
    """Fact Checker Node"""

    progress.start_node("Fact Checker")

    try:
        fact_checker = FactCheckerAgent()

        state["verified_data"] = fact_checker.verify(
            state["research_data"]
        )

        return state

    finally:
        progress.finish_node()


def writer_node(state: ResearchState) -> ResearchState:
    """Writer Node"""

    progress.start_node("Writer")

    try:
        writer = WriterAgent()

        state["report"] = writer.writer(
            state["verified_data"]
        )

        return state

    finally:
        progress.finish_node()


def citation_node(state: ResearchState) -> ResearchState:
    """Citation Node"""

    progress.start_node("Citation")

    try:
        citation = CitationAgent()

        state["cited_report"] = citation.generate(
            report=state["report"],
            sources=state["sources"],
            style=state["citation_style"],
        )

        return state

    finally:
        progress.finish_node()


def reviewer_node(state: ResearchState) -> ResearchState:
    """Reviewer Node"""

    progress.start_node("Reviewer")

    try:
        reviewer = ReviewerAgent()

        state["reviewed_report"] = reviewer.review(
            state["cited_report"]
        )

        return state

    finally:
        progress.finish_node()


def pdf_node(state: ResearchState) -> ResearchState:
    """PDF Generator Node"""

    progress.start_node("PDF Generator")

    try:
        pdf_generator = PDFGeneratorAgent()

        state["pdf_path"] = pdf_generator.generate(
            state["reviewed_report"]
        )

        return state

    finally:
        progress.finish_node()