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

    if not report.pdf_path:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF not available for this report.",
        )

    if not os.path.exists(report.pdf_path):

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF file not found on server.",
        )

    return FileResponse(
        path=report.pdf_path,
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

