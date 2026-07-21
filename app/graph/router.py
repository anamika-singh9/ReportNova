from app.graph.state import ResearchState


def research_router(state: ResearchState):
    """
    Decide whether to continue after research.
    """

    research = state.get("research_data")

    if research and len(research.strip()) > 20:
        return "continue"

    return "stop"


def fact_check_router(state: ResearchState):
    """
    Decide whether the report passed fact checking.
    """

    verified = state.get("verified_data")

    if verified and len(verified.strip()) > 20:
        return "continue"

    return "stop"