from __future__ import annotations


def cluster_aspects(aspects: list[str]) -> dict[str, list[str]]:
    return {"product_experience": sorted(set(aspects))}

