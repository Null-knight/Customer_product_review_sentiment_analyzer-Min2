from __future__ import annotations


EMOTION_TERMS = {
    "joy": {"happy", "love", "excellent", "great", "amazing", "perfect"},
    "anger": {"angry", "hate", "worst", "terrible", "awful"},
    "disappointment": {"disappointed", "stale", "broken", "poor", "bad"},
    "trust": {"fresh", "quality", "reliable", "recommend"},
}


def detect_emotion(text: str) -> str:
    lowered = set((text or "").lower().split())
    scores = {emotion: len(words & lowered) for emotion, words in EMOTION_TERMS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "neutral"

