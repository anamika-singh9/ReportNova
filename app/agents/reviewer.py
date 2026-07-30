from app.llms.model_factory import get_model
from app.utils.logger import logger
from app.utils.exceptions import ModelError

class ReviewerAgent:
    """
    Reviewer Agent

    Responsibility:
    - Review the generated report.
    - Improve grammar and readability.
    - Improve structure and consistency.

    It DOES NOT:
    - Perform research.
    - Verify facts.
    - Generate new information.
    """

    def __init__(self):
        self.llm = get_model()

    def review(self, report: str) -> str:
        """
        Review and improve the generated report.
        """

        prompt = f"""
You are a senior academic editor.

Your task is to review the following research report.

Research Report:

{report}

Check for:

1. Grammar mistakes
2. Spelling mistakes
3. Poor sentence structure
4. Repeated information
5. Logical flow
6. Professional tone
7. Heading consistency
8. Formatting consistency

Rules:

- Preserve the original meaning.
- Do NOT add new facts.
- Do NOT perform additional research.
- Do NOT remove the References section.
- Return ONLY the final improved report.
"""

        try:

            logger.info("Reviewing report.")

            response = self.llm.invoke(prompt)

            logger.info("Review completed.")

            return response.text

        except Exception as e:

            logger.exception("Reviewer agent failed.")

            raise ModelError(
                "Unable to review report."
            ) from e