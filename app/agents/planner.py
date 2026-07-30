from app.llms.model_factory import get_model
from app.utils.logger import logger
from app.utils.exceptions import ModelError

class PlannerAgent:
    """
    Planner Agent 
    
    Responsibility:
    - Understant the user's request.
    - Break it into research tasks.
    - Create a structured research plan.

    It Does not:
    - Search the web
    - Read PDFs
    - Verify facts
    - Write reports
    """

    def __init__(self):
        self.llm=get_model()
        
    def plan(self, topic: str) -> str:
        prompt = f"""

        You are an expert Research Planner.

        Your job is ONLY to create a research plan.

        Given the user's topic, generate:

        1. Main research objective.
        2. Key questions that should be answered.
        3. Important subtopics to research.
        4. Suggested report structure.

        Do NOT answer the topic.
        Do NOT provide explanations.
        Do NOT perform research.

        User Topic:
        {topic}

        """
        try:

            logger.info("Research planning started.")

            response = self.llm.invoke(prompt)

            logger.info("Research planning completed.")

            return response.text

        except Exception as e:

            logger.exception("Planner agent failed.")

            raise ModelError(
                "Unable to create research plan."
            ) from e