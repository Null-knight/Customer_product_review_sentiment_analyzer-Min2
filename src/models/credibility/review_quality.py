from __future__ import annotations


def review_quality_score(text: str) -> float:
    words = (text or "").split()
    length_score = min(0.6, len(words) / 80)
    detail_terms = {"taste", "packaging", "delivery", "quality", "price", "fresh", "flavor"}
    detail_score = min(0.4, len(set(words) & detail_terms) * 0.1)
    return round(length_score + detail_score, 3)

