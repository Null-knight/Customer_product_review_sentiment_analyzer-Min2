from __future__ import annotations


def detect_script(text: str) -> str:
    if any("\u0900" <= char <= "\u097f" for char in text):
        return "devanagari"
    if any("\u0980" <= char <= "\u09ff" for char in text):
        return "bengali"
    if any("\u0b80" <= char <= "\u0bff" for char in text):
        return "tamil"
    if any("\u0c00" <= char <= "\u0c7f" for char in text):
        return "telugu"
    return "latin"

