from __future__ import annotations


ASPECT_TERMS = {
    "taste": {"taste", "flavor", "sweet", "salty", "spicy"},
    "packaging": {"package", "packaging", "box", "sealed", "leak"},
    "delivery": {"delivery", "shipping", "arrived", "late", "fast"},
    "price": {"price", "cost", "cheap", "expensive", "value"},
    "quality": {"quality", "fresh", "stale", "broken", "good", "bad"},
}


def extract_aspects(text: str) -> list[str]:
    tokens = set((text or "").lower().split())
    return [aspect for aspect, terms in ASPECT_TERMS.items() if tokens & terms]

