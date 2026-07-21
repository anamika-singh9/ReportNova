from pydantic import BaseModel


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    topic: str
    report: str
    pdf_path: str