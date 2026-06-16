from __future__ import annotations


POSITIVE_WORDS = {"good", "great", "excellent", "amazing", "love", "best", "perfect", "fresh", "tasty"}
NEGATIVE_WORDS = {"bad", "terrible", "awful", "worst", "stale", "broken", "disappointed", "hate", "poor"}


def lexicon_sentiment_features(text: str) -> dict[str, float]:
    tokens = set((text or "").lower().split())
    positive = len(tokens & POSITIVE_WORDS)
    negative = len(tokens & NEGATIVE_WORDS)
    return {"positive_hits": float(positive), "negative_hits": float(negative), "lexicon_score": float(positive - negative)}

