from __future__ import annotations

import json
from pathlib import Path

import joblib

from src.utils.config import MODEL_DIR


class RatingPredictor:
    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or MODEL_DIR / "sentiment" / "sentiment_model.pkl"
        self.metadata_path = self.model_path.with_name("sentiment_metadata.json")
        if not self.model_path.exists():
            raise FileNotFoundError("Sentiment model not found. Run `python train.py` first.")
        self.model = joblib.load(self.model_path)
        self.metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))

    def predict(self, text: str) -> dict:
        label = str(self.model.predict([text])[0])
        probabilities = self.model.predict_proba([text])[0]
        classes = [str(item) for item in self.model.classes_]
        scores = {cls: round(float(prob), 4) for cls, prob in zip(classes, probabilities)}
        star = {"negative": 1, "neutral": 3, "positive": 5}.get(label, 3)
        return {
            "sentiment": label,
            "predicted_rating": star,
            "sentiment_scores": scores,
            "confidence": max(scores.values()) if scores else 0.0,
            "model_name": self.metadata.get("model_name", "unknown"),
        }

