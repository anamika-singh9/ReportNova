from app.llms.model_factory import get_model

class ReviewerAgent:
    """
    Reviewer Agent 
    
    Responsibility:
    - Review the generated report.
    - Improve quality and readability.
    - Check structure and consistency.

    It DOES NOT:
    - Perform research.
    - Verify external facts.
    - Generate new information.
    """

    def __init__(self):
        self.llm = get_model()

    def review(self, report: str)->str:
        """
        Review and improve a research report.
        """

        prompt = f"""

        You are an expert research report reviewer.

        Review the following report and improve it.

        Report:

        {report}

        Check for:

        1. Grammer mistakes
        2. Poor sentence structure
        3. Repeated information
        4. Missing logical connections
        5. Unprofessional language
        6. Formatting issues

        Rules:
        - Preserve the original meaning.
        - Do not add new facts.
        - Do not perform new research.
        - Return only the improved final report.

        """

        response = self.llm.invoke(prompt)

        return response.content[0]["text"]