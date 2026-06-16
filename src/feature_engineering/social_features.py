from __future__ import annotations


def helpfulness_ratio(numerator: int | float = 0, denominator: int | float = 0) -> float:
    denominator = float(denominator or 0)
    if denominator <= 0:
        return 0.0
    return round(float(numerator or 0) / denominator, 3)

