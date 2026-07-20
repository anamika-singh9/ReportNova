from app.llms.model_factory import get_model 

def generate_report(research_data: str) -> str:
    """
    Generate a structured report from research data.
    """
    model = get_model()

    prompt = f"""
    You are a professional research report writer.

    Create a detailed and well-structured report using the research information below.

    Research Information:
    {research_data}

    follow this format:

    # Title

    ## Introduction

    ## Key Findings

    ## Detailed Analysis

    ## Impact and Future Scope

    ## Conclusion

    ## Sources
        - include all source URLs provided in the research information.

    Write in a professional and easy-to-understand manner.

    """

    response = model.invoke(prompt)

    return response.text