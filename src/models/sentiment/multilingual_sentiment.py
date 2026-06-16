from __future__ import annotations

from src.feature_engineering.semantic_features import NEGATIVE_WORDS, POSITIVE_WORDS


def lexicon_sentiment(text: str) -> str:
    tokens = set((text or "").lower().split())
    positive = len(tokens & POSITIVE_WORDS)
    negative = len(tokens & NEGATIVE_WORDS)
    if positive > negative:
        return "positive"
    if negative > positive:
        return "negative"
    return "neutral"

