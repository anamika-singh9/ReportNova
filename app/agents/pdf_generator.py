import os
import markdown
from app.utils.logger import logger
from xhtml2pdf import pisa
from config.constants import (
    REPORT_DIR,
    DEFAULT_REPORT_NAME,
)
from app.utils.exceptions import PDFGenerationError

class PDFGeneratorAgent:
    """
    PDF Generator Agent

    Responsibility:
    - Convert Markdown to HTML.
    - Generate a professional PDF.
    """

    def generate(
        self,
        report: str,
        filename: str = DEFAULT_REPORT_NAME,
    ) -> str:

        os.makedirs(REPORT_DIR, exist_ok=True)

        pdf_path = os.path.join(
            REPORT_DIR,
            filename,
        )
        # Markdown → HTML
        html_body = markdown.markdown(
            report,
            extensions=[
                "tables",
                "fenced_code",
            ],
        )

        html = f"""
        <html>

        <head>

        <meta charset="UTF-8">

        <style>

        body {{
            font-family: Helvetica;
            font-size: 12px;
            line-height: 1.7;
            color: #222;
            margin: 40px;
        }}

        h1 {{
            color: #0F4C81;
            border-bottom: 2px solid #0F4C81;
            padding-bottom: 8px;
            font-size: 26px;
        }}

        h2 {{
            color: #145DA0;
            margin-top: 25px;
            font-size: 20px;
        }}

        h3 {{
            color: #333333;
            font-size: 16px;
        }}

        p {{
            text-align: justify;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            margin-bottom: 15px;
        }}

        table, th, td {{
            border: 1px solid #666;
        }}

        th {{
            background-color: #0F4C81;
            color: white;
            padding: 8px;
        }}

        td {{
            padding: 8px;
        }}

        ul {{
            margin-left: 20px;
        }}

        ol {{
            margin-left: 20px;
        }}

        code {{
            background-color: #eeeeee;
            padding: 2px 4px;
        }}

        pre {{
            background-color: #f5f5f5;
            padding: 10px;
            border: 1px solid #cccccc;
        }}

        blockquote {{
            border-left: 5px solid #0F4C81;
            padding-left: 15px;
            color: gray;
        }}

        </style>

        </head>

        <body>

        {html_body}

        </body>

        </html>
        """

        try:

            logger.info("Generating PDF.")

            with open(pdf_path, "wb") as pdf_file:

                pdf = pisa.CreatePDF(
                    src=html,
                    dest=pdf_file,
                )

            if pdf.err:
                raise PDFGenerationError(
                    "PDF generation failed."
                )

            logger.info(f"PDF saved to: {pdf_path}")

            return pdf_path

        except Exception as e:

            logger.exception("PDF generation failed.")

            raise PDFGenerationError(
                "Unable to generate PDF."
            ) from e