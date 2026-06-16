from __future__ import annotations

import os

try:
    import psutil
except Exception:  # pragma: no cover
    psutil = None


def memory_snapshot() -> dict[str, float]:
    if psutil is None:
        return {"rss_mb": 0.0, "system_percent": 0.0}
    proc = psutil.Process(os.getpid())
    return {
        "rss_mb": round(proc.memory_info().rss / 1024 / 1024, 2),
        "system_percent": psutil.virtual_memory().percent,
    }

