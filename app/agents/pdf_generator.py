import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class PDFGeneratorAgent:

    def generate(
        self,
        report: str,
        filename: str = "research_report.pdf"
    ) -> str:

        output_dir = "app/output"

        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(
            output_dir,
            filename
        )

        pdf = SimpleDocTemplate(file_path)

        styles = getSampleStyleSheet()

        story = []

        for line in report.split("\n"):
            if line.strip():
                story.append(
                    Paragraph(
                        line,
                        styles["BodyText"]
                    )
                )
                story.append(
                    Spacer(1, 12)
                )

        pdf.build(story)

        return file_path