from __future__ import annotations


PRODUCT_TERMS = {"taste", "product", "delivery", "package", "quality", "price", "food", "flavor", "fresh"}


def off_topic_score(text: str) -> float:
    tokens = set((text or "").lower().split())
    return 0.5 if tokens and not (tokens & PRODUCT_TERMS) else 0.0

