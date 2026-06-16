from __future__ import annotations

from difflib import SequenceMatcher


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, left or "", right or "").ratio()


def duplicate_score(text: str, recent_texts: list[str] | None = None) -> float:
    if not recent_texts:
        return 0.0
    return round(max(similarity(text, other) for other in recent_texts), 3)

