from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from src.models.aspect_mining.comparative_analyzer import has_comparative_opinion
from src.models.aspect_mining.opinion_mining import aspect_sentiment
from src.models.credibility.review_quality import review_quality_score
from src.models.credibility.user_scorer import user_credibility_score
from src.models.ensemble.stacking_classifier import final_verdict
from src.models.fake_detection.ensemble import fake_review_score
from src.models.sentiment.emotion_detector import detect_emotion
from src.models.sentiment.rating_predictor import RatingPredictor
from src.models.sentiment.sarcasm_detector import sarcasm_score
from src.models.spam_detection.duplicate_detector import duplicate_score
from src.models.spam_detection.off_topic import off_topic_score
from src.models.spam_detection.promotional_spam import promotional_spam_score
from src.preprocessing.pipeline import preprocess_review
from src.utils.audit_logger import append_jsonl
from src.utils.metrics import metrics


@dataclass
class ReviewVerdict:
    review_id: str
    decision: str
    sentiment: str
    predicted_rating: int
    emotion: str
    fake_score: float
    spam_score: float
    quality_score: float
    legit_probability: float
    aspects: dict[str, str]
    language: str
    reason: str
    processing_time_ms: float


class StreamReviewProcessor:
    """Real-time review processing pipeline for API and dashboard calls."""

    def __init__(self, sentiment_model: RatingPredictor | None = None) -> None:
        self.sentiment_model = sentiment_model or RatingPredictor()
        self.recent_reviews: list[str] = []

    def process_review(self, review: dict[str, Any]) -> ReviewVerdict:
        start = time.perf_counter()
        text = f"{review.get('summary', '')} {review.get('text', '')}".strip()
        preprocessed = preprocess_review(text)
        user_review_count = int(review.get("user_review_count", 0) or 0)
        avg_helpfulness = float(review.get("avg_helpfulness", 0) or 0)
        avg_rating = float(review.get("user_avg_rating", review.get("rating", 3)) or 3)

        sentiment = self.sentiment_model.predict(preprocessed.cleaned_text)
        credibility = user_credibility_score(user_review_count, avg_helpfulness, avg_rating)
        quality = review_quality_score(preprocessed.cleaned_text)
        fake = fake_review_score(preprocessed.cleaned_text, user_credibility=credibility)
        spam = max(
            promotional_spam_score(preprocessed.cleaned_text),
            off_topic_score(preprocessed.cleaned_text),
            duplicate_score(preprocessed.cleaned_text, self.recent_reviews),
        )
        verdict = final_verdict(fake, spam, quality)
        self.recent_reviews.append(preprocessed.cleaned_text)
        self.recent_reviews = self.recent_reviews[-1000:]

        result = ReviewVerdict(
            review_id=str(review.get("review_id") or review.get("id") or "manual"),
            decision=verdict["decision"],
            sentiment=sentiment["sentiment"],
            predicted_rating=sentiment["predicted_rating"],
            emotion=detect_emotion(preprocessed.cleaned_text),
            fake_score=fake,
            spam_score=round(spam, 3),
            quality_score=quality,
            legit_probability=verdict["legit_probability"],
            aspects=aspect_sentiment(preprocessed.cleaned_text),
            language=preprocessed.language,
            reason=verdict["reason"]
            + ("; comparative opinion found" if has_comparative_opinion(preprocessed.cleaned_text) else ""),
            processing_time_ms=round((time.perf_counter() - start) * 1000, 2),
        )
        metrics.inc(f"decision.{result.decision.lower()}")
        append_jsonl("predictions.jsonl", {"review": review, "result": result.__dict__})
        return result

