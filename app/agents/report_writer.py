from app.llms.model_factory import get_model 

class WriterAgent:
    """
    Write Agent

    Responsibility:
    - Convert Verified research notes into a professional report.
    - Structure the information clearly.

    It DOES NOT:
    - Perform research.
    - Verify facts.
    - Reivew the final report.
    """
    
    def __init__(self):
        self.llm = get_model()

    def writer(self, research_data: str) -> str:
        """
        Generate a structured research report.
        """

        prompt = f"""

        You are a professional research report writer.

        Your task is to create a detailed reprot using ONLY the verified reasearch information provided.

        verified Research Information:

        {research_data}

        Follow this structure:

        # Title

        ## Introduction

        ## Key Findings

        ## Detailed Analysis

        ## Impact and Future Scope

        ## Conclusion

        ## Sources

        Rules:
        - Keep the report professional and easy to understand.
        - Do not add usupported information.
        - Maintain logical flow between sections.
        - Use clear explanations.

        """

        response = self.llm.invoke(prompt)

        return response.text