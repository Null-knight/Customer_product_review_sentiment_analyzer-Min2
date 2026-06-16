from __future__ import annotations

from src.feature_engineering.semantic_features import NEGATIVE_WORDS, POSITIVE_WORDS
from src.models.aspect_mining.ner_extractor import extract_aspects


def aspect_sentiment(text: str) -> dict[str, str]:
    tokens = set((text or "").lower().split())
    sentiment = "neutral"
    if len(tokens & POSITIVE_WORDS) > len(tokens & NEGATIVE_WORDS):
        sentiment = "positive"
    elif len(tokens & NEGATIVE_WORDS) > len(tokens & POSITIVE_WORDS):
        sentiment = "negative"
    return {aspect: sentiment for aspect in extract_aspects(text)}

