from src.feature_engineering.linguistic_features import linguistic_features
from src.models.aspect_mining.ner_extractor import extract_aspects


def test_linguistic_features_count_words() -> None:
    features = linguistic_features("fresh taste and good packaging")
    assert features["word_count"] == 5


def test_aspect_extraction_finds_packaging() -> None:
    assert "packaging" in extract_aspects("The packaging was clean and sealed")

