from app.llms.model_factory import get_model
from app.utils.logger import logger
from app.utils.exceptions import ReportGenerationError

class WriterAgent:
    def __init__(self):
        
        self.llm = get_model()

    def writer(self, research_data: str) -> str:
        """
        Generate a structured research report.
        """

        prompt = f"""
    You are a professional AI Research Report Writer.

    You have been provided with verified research information collected from:

    1. Retrieved PDF context (highest priority)
    2. Web search results (secondary source)

    Your responsibility is to transform the research into a professional report.

    Guidelines:

    - Use the PDF context as the primary source whenever it is available.
    - Use web search information only to complement or expand missing details.
    - Never contradict information found in the PDF.
    - Avoid repeating the same information.
    - Do not invent facts.
    - Maintain a logical flow between sections.
    - Write in a clear, professional, and easy-to-understand style.

    Verified Research Information:

    {research_data}

    Create the report using the following structure.

    # Title

    ## Executive Summary

    ## Introduction

    ## Key Concepts

    ## Detailed Analysis

    ## Applications

    ## Advantages

    ## Challenges

    ## Future Scope

    ## Conclusion

    ## References

    Format the report in Markdown.
    """
        try:

            logger.info("Generating research report.")

            response = self.llm.invoke(prompt)

            logger.info("Report generated successfully.")

            return response.text

        except Exception as e:

            logger.exception("Report generation failed.")

            raise ReportGenerationError(
                "Unable to generate report."
            ) from e