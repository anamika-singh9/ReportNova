from app.llms.model_factory import get_model
from app.utils.logger import logger
from app.utils.exceptions import ModelError

class FactCheckerAgent:
    """
    Fact Checker Agent

    Responsibility:
    - Review the research notes.
    - Remove duplicate information.
    - Identify unsupported or weak claims.
    - Organize the verified information.

    It DOES NOT:
    - Search the web.
    - Read PDFs
    -Write the final report.
    """

    def __init__(self):
        self.llm = get_model()

    def verify(self, research_notes: str) -> str:
        prompt = f"""

        You are given research notes collected from different sources.

        Your tasks are:

        1. Remove duplicate information.
        2. Organize related information together.
        3. Flag any claims that appear unsupported or uncertain.
        4. Keep only information supported by the provided notes.
        5. Do NOT add new information.
        6. Do NOT write a report.

        Return clean, verified research notes.

        Research Notes:

        {research_notes}

        """

        try:

            logger.info("Fact checking started.")

            response = self.llm.invoke(prompt)

            logger.info("Fact checking completed.")

            return response.text

        except Exception as e:

            logger.exception("Fact Checker failed.")

            raise ModelError(
                "Unable to verify research."
            ) from e