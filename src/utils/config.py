from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_REVIEWS = DATA_DIR / "raw" / "amazon_reviews" / "Reviews.csv"
RAW_FLIPKART_REVIEWS = DATA_DIR / "raw" / "flipkart_reviews" / "Dataset-SA.csv"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = DATA_DIR / "models"
LOG_DIR = DATA_DIR / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"
PROJECT_AUTHOR = "Rahul Roy"
PROJECT_STARTED_ON = "February 12, 2026"


@dataclass(frozen=True)
class Thresholds:
    fake_block_threshold: float = 0.75
    fake_review_threshold: float = 0.55
    spam_threshold: float = 0.55
    low_quality_threshold: float = 0.35
    min_review_words: int = 4


def load_yaml(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return default or {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_thresholds() -> Thresholds:
    data = load_yaml(CONFIG_DIR / "thresholds.yaml")
    return Thresholds(**{**Thresholds().__dict__, **data})
