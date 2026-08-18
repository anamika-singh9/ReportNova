from datetime import datetime

from pydantic import BaseModel


class ReportResponse(BaseModel):

    id: int
    topic: str
    citation_style: str
    report_content: str
    sources: str | None
    pdf_path: str | None
    created_at: datetime


class ReportListResponse(BaseModel):

    id: int
    topic: str
    citation_style: str
    created_at: datetime


class GenerateReportResponse(BaseModel):

    status: str
    report_id: int
    topic: str
    citation_style: str
    report: str
    pdf_path: str | None
    sources: str | None