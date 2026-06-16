from __future__ import annotations


def review_bombing_score(recent_negative_count: int = 0) -> float:
    return min(1.0, recent_negative_count / 25)

