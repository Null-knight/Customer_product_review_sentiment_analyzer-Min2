from __future__ import annotations


def has_comparative_opinion(text: str) -> bool:
    lowered = (text or "").lower()
    return any(term in lowered for term in ["better than", "worse than", "compared to", "more than", "less than"])

