from __future__ import annotations


def campaign_risk(product_review_count_recent: int = 0, average_rating_recent: float = 0.0) -> float:
    if product_review_count_recent >= 20 and average_rating_recent >= 4.7:
        return 0.7
    if product_review_count_recent >= 20 and average_rating_recent <= 1.5:
        return 0.65
    return 0.0

