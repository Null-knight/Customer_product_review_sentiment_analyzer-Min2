from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{product_id}/summary")
def product_summary(product_id: str) -> dict:
    return {"product_id": product_id, "message": "Run batch processing to build product-level summaries."}

