from __future__ import annotations

from pathlib import Path

from src.models.sentiment.rating_predictor import RatingPredictor
from src.utils.config import MODEL_DIR


def load_sentiment_model(model_dir: Path = MODEL_DIR) -> RatingPredictor:
    return RatingPredictor(model_dir / "sentiment" / "sentiment_model.pkl")

