from __future__ import annotations

from fastapi import APIRouter

from src.models.credibility.user_scorer import user_credibility_score

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/credibility")
def user_credibility(user_id: str, review_count: int = 0, avg_helpfulness: float = 0.0) -> dict:
    return {"user_id": user_id, "credibility": user_credibility_score(review_count, avg_helpfulness)}

