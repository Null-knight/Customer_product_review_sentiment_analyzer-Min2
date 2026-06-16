from __future__ import annotations

import argparse

import pandas as pd

from src.pipeline.batch_processor import process_dataframe
from src.utils.config import RAW_REVIEWS


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a small batch evaluation.")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    df = pd.read_csv(RAW_REVIEWS, nrows=args.limit)
    results = process_dataframe(df, limit=args.limit)
    decisions = {}
    for row in results:
        decisions[row["decision"]] = decisions.get(row["decision"], 0) + 1
    print({"processed": len(results), "decisions": decisions})


if __name__ == "__main__":
    main()

