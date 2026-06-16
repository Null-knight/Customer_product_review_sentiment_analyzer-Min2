from __future__ import annotations

from datetime import datetime, timezone


def unix_time_features(timestamp: int | float | None) -> dict[str, float]:
    if not timestamp:
        return {"review_year": 0.0, "review_month": 0.0, "review_hour": 0.0}
    dt = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
    return {"review_year": float(dt.year), "review_month": float(dt.month), "review_hour": float(dt.hour)}

