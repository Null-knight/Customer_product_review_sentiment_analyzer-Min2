from __future__ import annotations


def user_behavior_features(user_review_count: int = 0, avg_rating: float = 0.0) -> dict[str, float]:
    return {
        "user_review_count": float(user_review_count),
        "user_avg_rating": round(float(avg_rating or 0), 3),
        "new_user_flag": 1.0 if user_review_count <= 1 else 0.0,
    }

