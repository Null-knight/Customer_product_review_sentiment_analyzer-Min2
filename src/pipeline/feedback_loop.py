from __future__ import annotations

from src.utils.audit_logger import append_jsonl


def record_feedback(review_id: str, label: str, notes: str = "") -> None:
    append_jsonl("feedback.jsonl", {"review_id": review_id, "label": label, "notes": notes})

