from typing import TypedDict, Optional

class ResearchState(TypedDict):
    topic:str 
    # planner output
    plan : Optional[str]

    # Researcher output
    research_data : Optional[str]

    # Fact checker output
    verified_data : Optional[str]

    # Writer output
    report : Optional[str]

    # Reviewer Output
    reviewed_report : Optional[str]

    # PDF output
    pdf_path : Optional[str]




    