from __future__ import annotations


EMOJI_MAP = {
    "😀": " happy ",
    "😊": " happy ",
    "😍": " love ",
    "😡": " angry ",
    "😞": " disappointed ",
    "😭": " sad ",
    "👍": " good ",
    "👎": " bad ",
}


def replace_emojis(text: str) -> str:
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    return text

