from __future__ import annotations

from fastapi import APIRouter

from src.utils.metrics import metrics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/metrics")
def get_metrics() -> dict[str, int]:
    return metrics.snapshot()

