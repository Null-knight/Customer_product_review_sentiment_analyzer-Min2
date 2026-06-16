from __future__ import annotations


COMMON_FIXES = {"recieved": "received", "definately": "definitely", "produc": "product"}


def correct_common_misspellings(text: str) -> str:
    return " ".join(COMMON_FIXES.get(word, word) for word in text.split())

