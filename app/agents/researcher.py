from app.tools.tavily_search import search_web

def research(topic: str) -> str:
    """
    Research a topic using external sources.

    Responsibility:
    - Collect information.
    - Do NOT write the final report.
    - Do NOT verify facts.
    """

    # step 1: search the web
    web_results = search_web(topic)

    research_notes = f"""
    Research Topic:
    {topic}

    ================
    WEB RESEARCH
    =================
    {web_results}
    """
    
    return research_notes