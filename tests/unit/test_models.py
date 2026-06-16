from src.models.fake_detection.ensemble import fake_review_score
from src.models.spam_detection.promotional_spam import promotional_spam_score


def test_spam_score_detects_promotional_text() -> None:
    assert promotional_spam_score("buy now free discount offer") > 0.5


def test_fake_score_stays_bounded() -> None:
    score = fake_review_score("in conclusion this product offers a delightful experience", user_credibility=0.2)
    assert 0 <= score <= 1

