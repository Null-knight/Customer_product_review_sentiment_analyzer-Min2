from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from scripts.prepare_data import prepare_data
from src.utils.config import MODEL_DIR, PROCESSED_DIR, load_yaml, CONFIG_DIR


def train_sentiment(max_rows: int = 120000) -> dict:
    cleaned_path = PROCESSED_DIR / "reviews_cleaned.csv"
    if cleaned_path.exists():
        df = pd.read_csv(cleaned_path)
        if max_rows:
            df = df.sample(frac=1.0, random_state=42).head(max_rows)
    else:
        df = prepare_data(max_rows)

    params = load_yaml(CONFIG_DIR / "model_params.yaml").get("sentiment", {})
    x_train, x_test, y_train, y_test = train_test_split(
        df["clean_text"].fillna(""),
        df["sentiment_label"],
        test_size=float(params.get("test_size", 0.2)),
        random_state=int(params.get("random_state", 42)),
        stratify=df["sentiment_label"],
    )
    model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=int(params.get("max_features", 50000)),
                    ngram_range=(int(params.get("ngram_min", 1)), int(params.get("ngram_max", 2))),
                    min_df=2,
                ),
            ),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    report = classification_report(y_test, pred, output_dict=True, zero_division=0)
    metadata = {
        "model_name": "tfidf_logistic_regression_sentiment",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "rows": int(len(df)),
        "accuracy": float(accuracy_score(y_test, pred)),
        "macro_f1": float(f1_score(y_test, pred, average="macro")),
        "classification_report": report,
    }
    model_dir = MODEL_DIR / "sentiment"
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_dir / "sentiment_model.pkl")
    (model_dir / "sentiment_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Train review analyzer models.")
    parser.add_argument("--max-rows", type=int, default=120000)
    args = parser.parse_args()
    metadata = train_sentiment(args.max_rows)
    print("Training complete")
    print(f"Rows: {metadata['rows']}")
    print(f"Accuracy: {metadata['accuracy']:.4f}")
    print(f"Macro F1: {metadata['macro_f1']:.4f}")


if __name__ == "__main__":
    main()
