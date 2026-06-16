from __future__ import annotations


def user_credibility_score(review_count: int = 0, avg_helpfulness: float = 0.0, avg_rating: float = 3.0) -> float:
    history_score = min(0.5, review_count / 50)
    helpfulness_score = min(0.3, max(0.0, avg_helpfulness) * 0.3)
    rating_penalty = 0.2 if avg_rating in {1.0, 5.0} and review_count < 3 else 0.0
    return round(max(0.0, min(1.0, 0.3 + history_score + helpfulness_score - rating_penalty)), 3)

