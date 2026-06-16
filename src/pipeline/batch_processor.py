from __future__ import annotations

import pandas as pd

from src.pipeline.stream_processor import StreamReviewProcessor


def process_dataframe(df: pd.DataFrame, limit: int = 1000) -> list[dict]:
    processor = StreamReviewProcessor()
    results = []
    for row in df.head(limit).to_dict(orient="records"):
        review = {
            "review_id": row.get("Id"),
            "product_id": row.get("ProductId"),
            "user_id": row.get("UserId"),
            "rating": row.get("Score"),
            "summary": row.get("Summary"),
            "text": row.get("Text"),
        }
        results.append(processor.process_review(review).__dict__)
    return results

