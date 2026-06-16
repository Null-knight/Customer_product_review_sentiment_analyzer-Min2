from __future__ import annotations

PROMO_TERMS = {"buy now", "discount", "coupon", "free", "promo", "offer", "click", "subscribe"}


def promotional_spam_score(text: str) -> float:
    lowered = (text or "").lower()
    hits = sum(1 for term in PROMO_TERMS if term in lowered)
    return min(1.0, hits / 3)

