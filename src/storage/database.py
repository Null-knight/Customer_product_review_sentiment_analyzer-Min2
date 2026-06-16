from __future__ import annotations

import sqlite3
from pathlib import Path

from src.utils.config import DATA_DIR


DB_PATH = DATA_DIR / "processed" / "review_analyzer.db"


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS review_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id TEXT,
            product_id TEXT,
            user_id TEXT,
            decision TEXT,
            sentiment TEXT,
            fake_score REAL,
            spam_score REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return conn

