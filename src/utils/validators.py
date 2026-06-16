from __future__ import annotations


def clamp_rating(value: int | float | None) -> int | None:
    if value is None:
        return None
    return max(1, min(5, int(value)))


def require_text(text: str) -> str:
    cleaned = (text or "").strip()
    if not cleaned:
        raise ValueError("Review text is required")
    return cleaned

