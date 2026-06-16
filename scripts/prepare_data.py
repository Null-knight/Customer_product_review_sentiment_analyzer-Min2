from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.pipeline import preprocess_review
from src.utils.config import PROCESSED_DIR, RAW_FLIPKART_REVIEWS, RAW_REVIEWS


def sentiment_label(score: int) -> str:
    if score <= 2:
        return "negative"
    if score == 3:
        return "neutral"
    return "positive"


def _load_amazon(max_rows: int | None) -> pd.DataFrame:
    read_kwargs = {"usecols": ["Id", "ProductId", "UserId", "ProfileName", "HelpfulnessNumerator", "HelpfulnessDenominator", "Score", "Time", "Summary", "Text"]}
    if max_rows:
        read_kwargs["nrows"] = max_rows
    df = pd.read_csv(RAW_REVIEWS, **read_kwargs)
    df["source"] = "amazon"
    return df


def _load_flipkart(max_rows: int | None) -> pd.DataFrame:
    if not RAW_FLIPKART_REVIEWS.exists():
        return pd.DataFrame()
    read_kwargs = {"usecols": ["product_name", "product_price", "Rate", "Review", "Summary", "Sentiment"]}
    if max_rows:
        read_kwargs["nrows"] = max_rows
    raw = pd.read_csv(RAW_FLIPKART_REVIEWS, **read_kwargs)
    df = pd.DataFrame(
        {
            "Id": [f"flipkart-{i}" for i in range(1, len(raw) + 1)],
            "ProductId": raw["product_name"].fillna("flipkart-product").astype(str).str.slice(0, 80),
            "UserId": "flipkart-user",
            "ProfileName": "Flipkart Reviewer",
            "HelpfulnessNumerator": 0,
            "HelpfulnessDenominator": 0,
            "Score": pd.to_numeric(raw["Rate"], errors="coerce").fillna(3).clip(1, 5).astype(int),
            "Time": 0,
            "Summary": raw["Review"].fillna(""),
            "Text": raw["Summary"].fillna(""),
            "source": "flipkart",
        }
    )
    if "Sentiment" in raw:
        df["sentiment_label"] = raw["Sentiment"].fillna("").str.lower().replace({"neg": "negative", "pos": "positive"})
    return df


def prepare_data(max_rows: int | None = 120000, include_flipkart: bool = True) -> pd.DataFrame:
    amazon_rows = max_rows
    flipkart_rows = max(1000, max_rows // 4) if max_rows else None
    frames = [_load_amazon(amazon_rows)]
    if include_flipkart:
        flipkart = _load_flipkart(flipkart_rows)
        if not flipkart.empty:
            frames.append(flipkart)
    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["Text", "Score"]).copy()
    df["Summary"] = df["Summary"].fillna("")
    df["clean_text"] = [preprocess_review(f"{s} {t}").cleaned_text for s, t in zip(df["Summary"], df["Text"])]
    if "sentiment_label" not in df:
        df["sentiment_label"] = df["Score"].astype(int).map(sentiment_label)
    else:
        score_labels = df["Score"].astype(int).map(sentiment_label)
        df["sentiment_label"] = df["sentiment_label"].where(df["sentiment_label"].isin(["negative", "neutral", "positive"]), score_labels)
        df["sentiment_label"] = df["sentiment_label"].fillna(score_labels)
    df["helpfulness_ratio"] = df["HelpfulnessNumerator"] / df["HelpfulnessDenominator"].replace(0, pd.NA)
    df["helpfulness_ratio"] = df["helpfulness_ratio"].fillna(0)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DIR / "reviews_cleaned.csv", index=False)

    user_profiles = (
        df.groupby("UserId")
        .agg(review_count=("Id", "count"), avg_rating=("Score", "mean"), avg_helpfulness=("helpfulness_ratio", "mean"))
        .reset_index()
    )
    product_stats = (
        df.groupby("ProductId")
        .agg(review_count=("Id", "count"), avg_rating=("Score", "mean"), positive_rate=("sentiment_label", lambda s: (s == "positive").mean()))
        .reset_index()
    )
    user_profiles.to_csv(PROCESSED_DIR / "user_profiles.csv", index=False)
    product_stats.to_csv(PROCESSED_DIR / "product_stats.csv", index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and prepare Amazon review data.")
    parser.add_argument("--max-rows", type=int, default=120000)
    parser.add_argument("--no-flipkart", action="store_true", help="Only prepare the Amazon review CSV.")
    args = parser.parse_args()
    df = prepare_data(args.max_rows, include_flipkart=not args.no_flipkart)
    print(f"Prepared rows: {len(df)}")
    print(f"Output: {PROCESSED_DIR / 'reviews_cleaned.csv'}")


if __name__ == "__main__":
    main()
