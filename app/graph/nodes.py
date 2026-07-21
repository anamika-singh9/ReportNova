from app.graph.state import ResearchState

from app.agents.planner import PlannerAgent
from app.agents.researcher import research
from app.agents.fact_checker import FactCheckerAgent
from app.agents.report_writer import WriterAgent
from app.agents.reviewer import ReviewerAgent
from app.agents.pdf_generator import PDFGeneratorAgent


def planner_node(state: ResearchState) -> ResearchState:
    """Planner Node"""
    planner = PlannerAgent()
    state["plan"] = planner.plan(state["topic"])
    return state


def researcher_node(state: ResearchState) -> ResearchState:
    """Researcher Node"""
    state["research_data"] = research(state["topic"])
    return state


def fact_checker_node(state: ResearchState) -> ResearchState:
    """Fact Checker Node"""
    factChecker = FactCheckerAgent()
    state["verified_data"] = factChecker.verify(state["research_data"])
    return state


def writer_node(state: ResearchState) -> ResearchState:
    """Writer Node"""
    reportWriter = WriterAgent()
    state["report"] = reportWriter.writer(state["verified_data"])
    return state


def reviewer_node(state: ResearchState) -> ResearchState:
    """Reviewer Node"""
    reviewer = ReviewerAgent()
    state["reviewed_report"] = reviewer.review(state["report"])
    return state


def pdf_node(state: ResearchState) -> ResearchState:
    """PDF Generator Node"""
    PDFGenerator = PDFGeneratorAgent()
    state["pdf_path"] = PDFGenerator.generate(state["reviewed_report"])
    return state