from app.tools.tavily_search import search_web
from app.utils.logger import logger
from app.utils.exceptions import ResearchError

def research(topic: str) -> dict:
    
    """
    Research a topic using external sources.

    Responsibilities:
    - Search the web.
    - Collect research notes.
    - Collect source metadata.

    It DOES NOT:
    - Verify facts.
    - Write the report.
    - Generate citations.

    Returns:
    {
        "notes": str,
        "sources": list
    }
    """

    logger.info(f"Research started for topic: {topic}")

    try:

        web_result = search_web(topic)

        logger.info("Research completed.")

    except Exception as e:

        logger.exception("Research failed.")

        raise ResearchError(
            "Unable to collect research data."
        ) from e

    research_notes = f"""
Research Topic:
{topic}

========================
WEB RESEARCH
========================

{web_result["notes"]}
"""

    return {
        "notes": research_notes,
        "sources": web_result["sources"],
    }

