from typing import TypedDict, Optional


class ResearchState(TypedDict):
    # User Input
    topic: str
    citation_style: str

    # Planner
    plan: Optional[str]

    # Researcher
    research_data: Optional[str]
    sources: Optional[list]

    # Fact Checker
    verified_data: Optional[str]

    # Writer
    report: Optional[str]

    # Citation Agent
    cited_report: Optional[str]

    # Reviewer
    reviewed_report: Optional[str]

    # PDF
    pdf_path: Optional[str]