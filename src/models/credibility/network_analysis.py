from __future__ import annotations


def suspicious_network_score(shared_products: int = 0) -> float:
    return min(1.0, shared_products / 10)

