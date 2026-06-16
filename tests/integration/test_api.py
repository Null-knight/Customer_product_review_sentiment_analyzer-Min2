from src.api.schemas import ReviewRequest


def test_review_request_schema() -> None:
    payload = ReviewRequest(text="good product", rating=5)
    assert payload.rating == 5

