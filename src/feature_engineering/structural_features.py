from __future__ import annotations

import re


def structural_features(text: str) -> dict[str, float]:
    text = text or ""
    url_count = len(re.findall(r"https?://|www\.", text.lower()))
    uppercase_ratio = sum(1 for char in text if char.isupper()) / max(1, len(text))
    repeated_words = len(re.findall(r"\b(\w+)\s+\1\b", text.lower()))
    return {
        "url_count": float(url_count),
        "uppercase_ratio": round(uppercase_ratio, 3),
        "repeated_words": float(repeated_words),
    }

