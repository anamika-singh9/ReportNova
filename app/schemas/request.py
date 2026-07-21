from pydantic import BaseModel

class ReportRequest(BaseModel):
    topic: str