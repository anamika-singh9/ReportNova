from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.schemas.report import (
    ReportResponse,
    ReportListResponse,
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import User, Report
from app.auth.dependencies import get_current_user
from fastapi.responses import FileResponse
import os


from app.agents.pdf_generator import PDFGeneratorAgent
from fastapi.responses import Response

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


# ==========================================
# GET ALL REPORTS OF CURRENT USER
# ==========================================

@router.get(
    "/",
    response_model=list[ReportListResponse],
)
def get_my_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    reports = (
        db.query(Report)
        .filter(
            Report.user_id == current_user.id
        )
        .order_by(
            Report.created_at.desc()
        )
        .all()
    )

    return reports

# ==========================================
# DOWNLOAD REPORT PDF
# ==========================================


@router.get("/{report_id}/download")
def download_report_pdf(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.user_id == current_user.id,
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    # Agar disk pe PDF pehle se maujood hai, wahi bhejo (fast path)
    if report.pdf_path and os.path.exists(report.pdf_path):
        return FileResponse(
            path=report.pdf_path,
            media_type="application/pdf",
            filename=f"research_report_{report.id}.pdf",
        )

    # Warna (disk reset ho chuka hai) — content se fresh PDF banao
    pdf_generator = PDFGeneratorAgent()

    new_pdf_path = pdf_generator.generate(
        report=report.report_content,
        filename=f"research_report_{report.id}.pdf",
    )

    # Naya path DB mein update kar do, taaki agli baar fast path chale
    report.pdf_path = new_pdf_path
    db.commit()

    return FileResponse(
        path=new_pdf_path,
        media_type="application/pdf",
        filename=f"research_report_{report.id}.pdf",
    )


# ==========================================
# GET SINGLE REPORT
# ==========================================

@router.get(
    "/{report_id}",
    response_model=ReportResponse,
)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.user_id == current_user.id,
        )
        .first()
    )

    if not report:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    return report

# ==========================================
# DELETE REPORT
# ==========================================

@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.user_id == current_user.id,
        )
        .first()
    )

    if not report:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    db.delete(report)

    db.commit()

    return {
        "message": "Report deleted successfully."
    }

