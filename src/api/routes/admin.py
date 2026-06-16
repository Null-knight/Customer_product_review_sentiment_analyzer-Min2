from __future__ import annotations

from fastapi import APIRouter

from src.utils.config import LOG_DIR

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/recent-predictions")
def recent_predictions(limit: int = 20) -> list[str]:
    path = LOG_DIR / "predictions.jsonl"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[-limit:]

