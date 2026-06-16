from src.preprocessing.pipeline import preprocess_review


def test_preprocess_review_normalizes_text() -> None:
    result = preprocess_review("AWESOME!!!! gr8 product 😊")
    assert "great" in result.cleaned_text
    assert result.language in {"english", "hinglish"}

