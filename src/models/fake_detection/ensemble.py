from __future__ import annotations

from src.models.fake_detection.llm_detector import llm_generated_score
from src.models.spam_detection.promotional_spam import promotional_spam_score
from src.models.spam_detection.off_topic import off_topic_score


def fake_review_score(text: str, user_credibility: float = 0.7) -> float:
    low_credibility = max(0.0, 1.0 - user_credibility)
    score = (
        0.45 * llm_generated_score(text)
        + 0.25 * promotional_spam_score(text)
        + 0.15 * off_topic_score(text)
        + 0.15 * low_credibility
    )
    return round(min(1.0, score), 3)

