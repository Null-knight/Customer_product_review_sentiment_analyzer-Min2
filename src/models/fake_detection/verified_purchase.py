from __future__ import annotations


def verified_purchase_score(is_verified: bool | None) -> float:
    if is_verified is None:
        return 0.2
    return 0.0 if is_verified else 0.35

