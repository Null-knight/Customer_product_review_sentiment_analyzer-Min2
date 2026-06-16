from __future__ import annotations

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    review_id: str = "manual-review"
    product_id: str = "manual-product"
    user_id: str = "manual-user"
    rating: int | None = Field(default=None, ge=1, le=5)
    summary: str = ""
    text: str
    user_review_count: int = 0
    avg_helpfulness: float = 0.0
    user_avg_rating: float = 3.0


class FeedbackRequest(BaseModel):
    review_id: str
    label: str
    notes: str = ""

