from tavily import TavilyClient
from config.settings import settings

# Initialize Tavily client
client = TavilyClient(api_key=settings.TAVILY_API_KEY)


def search_web(query: str) -> dict:
    """
    Search the web using Tavily.

    Returns:
        {
            "notes": str,
            "sources": list
        }
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )

    research_notes = []

    sources = []

    for item in response.get("results", []):

        title = item.get("title", "")
        content = item.get("content", "")
        url = item.get("url", "")

        # -------- Metadata -------- #

        author = (
            item.get("author")
            or item.get("publisher")
            or item.get("source")
            or ""
        )

        published_date = (
            item.get("published_date")
            or item.get("published")
            or ""
        )

        favicon = item.get("favicon", "")

        # -------- Notes for Research Agent -------- #

        research_notes.append(
            f"""
Title: {title}

Content:
{content}

Source:
{url}
"""
        )

        # -------- Structured metadata -------- #

        sources.append(
            {
                "title": title,
                "url": url,
                "author": author,
                "published_date": published_date,
                "source": url,
                "favicon": favicon,
            }
        )

    return {
        "notes": "\n".join(research_notes),
        "sources": sources,
    }