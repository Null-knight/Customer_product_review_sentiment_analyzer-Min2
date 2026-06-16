from __future__ import annotations

from src.utils.audit_logger import append_jsonl


def log_request(path: str, method: str) -> None:
    append_jsonl("system_metrics.jsonl", {"path": path, "method": method})

