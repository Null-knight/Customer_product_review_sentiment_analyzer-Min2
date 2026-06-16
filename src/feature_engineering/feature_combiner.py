from __future__ import annotations

from src.feature_engineering.behavioral_features import user_behavior_features
from src.feature_engineering.linguistic_features import linguistic_features
from src.feature_engineering.semantic_features import lexicon_sentiment_features
from src.feature_engineering.social_features import helpfulness_ratio
from src.feature_engineering.structural_features import structural_features
from src.feature_engineering.temporal_features import unix_time_features


def combine_features(review: dict, user_review_count: int = 0, user_avg_rating: float = 0.0) -> dict[str, float]:
    text = f"{review.get('summary', '')} {review.get('text', '')}"
    features = {}
    features.update(linguistic_features(text))
    features.update(structural_features(text))
    features.update(lexicon_sentiment_features(text))
    features.update(unix_time_features(review.get("time")))
    features.update(user_behavior_features(user_review_count, user_avg_rating))
    features["helpfulness_ratio"] = helpfulness_ratio(
        review.get("helpfulness_numerator", 0), review.get("helpfulness_denominator", 0)
    )
    return features

