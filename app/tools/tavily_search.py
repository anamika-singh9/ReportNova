from tavily import TavilyClient
from config.settings import settings

# Initialize the Tavily client once 
client= TavilyClient(api_key = settings.TAVILY_API_KEY)

def search_web(query: str) -> str:
    """
    Search the web using Tavily.
    Args:
        query (str): Search query.
    Returns:
        str: Combined search results.
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )
    
    results = []

    for item in response.get("results", []):
        title = item.get("title", "")
        content = item.get("content", "")
        url = item.get("url", "")
        results.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"Source URL: {url}\n"
        )
    return "\n".join(results)