from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from src.utils.config import LOG_DIR


def append_jsonl(filename: str, payload: dict[str, Any]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    event = {"timestamp": datetime.now(timezone.utc).isoformat(), **payload}
    with (LOG_DIR / filename).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

