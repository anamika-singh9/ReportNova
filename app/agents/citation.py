from app.llms.model_factory import get_model
from app.utils.logger import logger
from app.utils.exceptions import CitationError

class CitationAgent:
    """
    Citation Agent

    Responsibility:
    - Generate professional academic citations.
    - Support APA and IEEE citation styles.
    - Append references to the report.

    It DOES NOT:
    - Perform research.
    - Verify facts.
    - Rewrite the report.
    - Review grammar.
    """

    def __init__(self):
        self.llm = get_model()

    def _format_sources(self, sources: list) -> str:
        """
        Convert source metadata into a clean format for the LLM.
        """

        formatted = []

        for source in sources:

            title = source.get("title", "Unknown Title")
            url = source.get("url", "Unknown URL")

            author = (
                source.get("author")
                or source.get("source")
                or source.get("domain")
                or "Unknown"
            )

            published = (
                source.get("published_date")
                or source.get("published")
                or "n.d."
            )

            formatted.append(
                    f"""
                Title: {title}
                Author: {author}
                Published: {published}
                URL: {url}
                """
                )

        return "\n".join(formatted)

    def generate(
        self,
        report: str,
        sources: list,
        style: str = "APA",
    ) -> str:
        """
        Append professional citations to the generated report.

        Args:
            report (str): Generated research report.
            sources (list): Source metadata collected during research.
            style (str): Citation style (APA / IEEE).

        Returns:
            str: Report with formatted references.
        """
        formatted_sources = self._format_sources(sources)

        prompt = f"""
You are an Academic Citation Specialist.

Your ONLY responsibility is to generate professional academic references.

Citation Style:
{style}

Research Report:

{report}

Source Metadata:

{formatted_sources}

Instructions:

1. Generate references ONLY from the provided source metadata.
2. Never invent authors.
3. If author is unavailable, use the organization or website name.
4. If publication date is unavailable:
   - APA -> use (n.d.)
   - IEEE -> omit the year if necessary.
5. Follow the selected citation style exactly.
6. Append a new section titled "References".
7. Do NOT modify the report.
8. Do NOT rewrite any paragraph.
9. Return the report followed by the references only.
"""

        try:

            logger.info("Generating citations.")

            response = self.llm.invoke(prompt)

            logger.info("Citation generation completed.")

            return response.text

        except Exception as e:

            logger.exception("Citation generation failed.")

            raise CitationError(
                "Unable to generate citations."
            ) from e