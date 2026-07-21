from fastapi import APIRouter

from app.api.schemas import (
    ResearchRequest,
    ResearchResponse,
)

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.post(
    "/research",
    response_model=ResearchResponse,
)
def research(request: ResearchRequest):

    # Temporary response
    return ResearchResponse(
        topic=request.topic,
        report="Report generation will be connected in the next step.",
        pdf_path="Not generated yet",
    )