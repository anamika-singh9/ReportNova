from app.llms.model_factory import get_model
from app.tools.tavily_search import search_web

# Initialize the LLM once
model = get_model()

def research(topic: str) -> str:
    """
    Preform research on a given topic using Tavily search and summarize it with Gemini.
    Args: 
        topic (str): The topic to research.
    Returns: 
        str: Structured research report.
    """

    # step 1: search the web
    web_results = search_web(topic)
    # step 2: Build the prompt
    prompt = f"""
    Your are an expert AI Research Assistant.

    Your task is to create a detailed research report using ONLY the information provided below.

    Research Topic:
    {topic}

    Web Search Results: 
    {web_results}

    Create a well-structured report with the following sections:

    1. Introduction
    2. Key Concepts
    3. Applications
    4. Advantages
    5. Challenges
    6. Future Scope
    7. Conclusion
    
    Keep the report factual, clear, and easy to understand.
    Do not make up information that is not supported by the search results.
    """

    # Step 3: Generate the report
    response = model.invoke(prompt)
    
    return response.content