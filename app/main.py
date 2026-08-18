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
    Depends,
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.auth import router as auth_router
from app.models import User, Report
from app.auth.dependencies import get_current_user

import os
import shutil

from app.utils.progress import progress
from app.services.rag_service import process_pdf
from app.utils.logger import logger
from config.constants import UPLOAD_DIR

from app.api.reports import router as reports_router

from app.schemas.report import GenerateReportResponse

os.makedirs(UPLOAD_DIR, exist_ok=True)


app = FastAPI(
    title="AI Research Report Generator",
    version="1.0",
    description="Agentic AI Research Report System",
)


app.include_router(auth_router)

app.include_router(reports_router)

graph = build_graph()
TOTAL_NODES = total_workflow_nodes()


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "AI Research Report Generator API is Running"
    }


# ==========================================
# PROGRESS
# ==========================================

@app.get("/progress")
def get_progress():

    return progress.get()


# ==========================================
# GENERATE REPORT
# ==========================================

@app.post(
    "/generate-report",
    response_model=GenerateReportResponse,
)
def generate_report(

    topic: str = Form(...),

    citation_style: str = Form("APA"),

    file: UploadFile | None = File(None),

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    try:

        # ==================================
        # PDF UPLOAD
        # ==================================

        if file:

            logger.info(
                f"Uploading PDF: {file.filename}"
            )

            pdf_path = os.path.join(
                UPLOAD_DIR,
                file.filename,
            )

            with open(
                pdf_path,
                "wb",
            ) as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer,
                )

            logger.info(
                "PDF uploaded successfully."
            )

            total_chunks = process_pdf(
                pdf_path
            )

            logger.info(
                f"Indexed {total_chunks} chunks."
            )


        # ==================================
        # LANGGRAPH WORKFLOW
        # ==================================

        logger.info(
            "Starting LangGraph workflow."
        )

        state = {
            "topic": topic,
            "citation_style": citation_style,
        }


        progress.reset()

        progress.start_workflow(
            total_nodes=TOTAL_NODES
        )


        try:

            result = graph.invoke(
                state
            )

        finally:

            progress.finish_workflow()


        logger.info(
            "LangGraph workflow completed."
        )


        # ==================================
        # SAVE REPORT TO DATABASE
        # ==================================

        new_report = Report(

            user_id=current_user.id,

            topic=topic,

            citation_style=citation_style,

            report_content=result.get(
                "reviewed_report",
                "",
            ),

            sources=str(
                result.get(
                    "sources",
                    [],
                )
            ),

            pdf_path=result.get(
                "pdf_path",
                "",
            ),
        )


        db.add(
            new_report
        )

        db.commit()

        db.refresh(
            new_report
        )


        logger.info(
            f"Report saved successfully "
            f"with ID: {new_report.id}"
        )


        # ==================================
        # RESPONSE
        # ==================================

        return {

            "status": "success",

            "report_id": new_report.id,

            "topic": topic,

            "citation_style": citation_style,

            "report": new_report.report_content,

            "pdf_path": new_report.pdf_path,

            "sources": new_report.sources,
        }


    except Exception:

        logger.exception(
            "Report generation failed."
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "Failed to generate the "
                "research report. Please try again."
            ),
        )