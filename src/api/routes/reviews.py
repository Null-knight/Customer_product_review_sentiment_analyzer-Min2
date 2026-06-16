from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.api.schemas import FeedbackRequest, ReviewRequest
from src.pipeline.feedback_loop import record_feedback
from src.pipeline.stream_processor import StreamReviewProcessor

router = APIRouter(prefix="/reviews", tags=["reviews"])


def get_processor() -> StreamReviewProcessor:
    from src.api.server_state import processor

    return processor


@router.post("/analyze")
def analyze_review(review: ReviewRequest) -> dict:
    try:
        return get_processor().process_review(review.model_dump()).__dict__
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/feedback")
def feedback(payload: FeedbackRequest) -> dict:
    record_feedback(payload.review_id, payload.label, payload.notes)
    return {"status": "recorded"}

