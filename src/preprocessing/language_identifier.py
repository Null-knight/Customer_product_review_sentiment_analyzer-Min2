from __future__ import annotations

from src.preprocessing.script_detector import detect_script


HINGLISH_MARKERS = {"acha", "accha", "mast", "bekar", "bakwas", "paisa", "kharab"}


def identify_language(text: str) -> str:
    script = detect_script(text)
    if script != "latin":
        return script
    tokens = set(text.lower().split())
    if tokens & HINGLISH_MARKERS:
        return "hinglish"
    return "english"

