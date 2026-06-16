from __future__ import annotations


def drift_warning(current_positive_rate: float, baseline_positive_rate: float, tolerance: float = 0.15) -> bool:
    return abs(current_positive_rate - baseline_positive_rate) > tolerance

