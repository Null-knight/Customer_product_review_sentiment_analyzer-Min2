from src.preprocessing.pipeline import preprocess_review


def test_preprocessing_is_fast_enough() -> None:
    assert preprocess_review("good product").cleaned_text == "good product"

