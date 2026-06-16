from src.models.sentiment.multilingual_sentiment import lexicon_sentiment


def test_lexicon_sentiment_positive() -> None:
    assert lexicon_sentiment("excellent fresh amazing product") == "positive"

