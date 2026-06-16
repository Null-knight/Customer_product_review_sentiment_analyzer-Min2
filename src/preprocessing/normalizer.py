from __future__ import annotations

import html
import re


SLANG = {
    "gr8": "great",
    "awsm": "awesome",
    "nyc": "nice",
    "bakwas": "bad",
    "acha": "good",
    "accha": "good",
    "mast": "great",
}


def normalize_text(text: str) -> str:
    """Normalize noisy review text while keeping sentiment-bearing words."""
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.lower()
    text = re.sub(r"(.)\1{3,}", r"\1\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    words = [SLANG.get(word, word) for word in text.split()]
    return " ".join(words)

