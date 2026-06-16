from __future__ import annotations


def calibrate_probability(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 4)

