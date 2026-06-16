from __future__ import annotations

from collections import Counter
from threading import Lock


class Metrics:
    def __init__(self) -> None:
        self._counter: Counter[str] = Counter()
        self._lock = Lock()

    def inc(self, key: str, amount: int = 1) -> None:
        with self._lock:
            self._counter[key] += amount

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return dict(self._counter)


metrics = Metrics()

