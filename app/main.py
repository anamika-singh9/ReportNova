from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.graph.workflow import build_graph

app = FastAPI(
    title="AI Research Report Generator",
    version="1.0",
    description="Agentic AI Research Report System"
)

graph = build_graph()


class ReportRequest(BaseModel):
    topic: str


@app.get("/")
def home():
    return {"message": "AI Research Report Generator API is Running"}


@app.post("/generate-report")
def generate_report(request: ReportRequest):
    try:
        state = {
            "topic": request.topic
        }

        result = graph.invoke(state)

        return {
            "status": "success",
            "topic": request.topic,
            "report": result.get("reviewed_report", ""),
            "pdf_path": result.get("pdf_path", "")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )