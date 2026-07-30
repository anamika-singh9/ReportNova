from app.graph.workflow import (
    build_graph,
    total_workflow_nodes,
)
from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
)
import os
import shutil
from app.utils.progress import progress
from app.services.rag_service import process_pdf
from app.utils.logger import logger
from config.constants import UPLOAD_DIR

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="AI Research Report Generator",
    version="1.0",
    description="Agentic AI Research Report System"
)

graph = build_graph()
TOTAL_NODES = total_workflow_nodes()

@app.get("/")
def home():
    return {"message": "AI Research Report Generator API is Running"}

@app.get("/progress")
def get_progress():
    """
    Returns current workflow progress.
    """
    return progress.get()

@app.post("/generate-report")
def generate_report(
    topic: str = Form(...),
    citation_style: str = Form("APA"),
    file: UploadFile | None = File(None),
):
    try:

        if file:

            logger.info(f"Uploading PDF: {file.filename}")

            pdf_path = os.path.join(
                UPLOAD_DIR,
                file.filename,
            )

            with open(pdf_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            logger.info("PDF uploaded successfully.")

            total_chunks = process_pdf(pdf_path)

            logger.info(f"Indexed {total_chunks} chunks.")

        logger.info("Starting LangGraph workflow.")

        state = {
            "topic": topic,
            "citation_style": citation_style,
        }

        progress.reset()

        progress.start_workflow(
            total_nodes=TOTAL_NODES
        )

        try:

            result = graph.invoke(state)

        finally:

            progress.finish_workflow()

        logger.info("LangGraph workflow completed.")


        return {
            "status": "success",
            "topic": topic,
            "citation_style": citation_style,
            "report": result.get("reviewed_report", ""),
            "pdf_path": result.get("pdf_path", ""),
            "sources": result.get("sources", []),
        }

    except Exception:

        logger.exception("Report generation failed.")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate the research report. Please try again."
        )


