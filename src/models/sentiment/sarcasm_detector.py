from __future__ import annotations


def sarcasm_score(text: str, rating: int | None = None) -> float:
    lowered = (text or "").lower()
    cues = ["yeah right", "great... not", "thanks for nothing", "just what i needed"]
    cue_score = 0.5 if any(cue in lowered for cue in cues) else 0.0
    mismatch = 0.25 if rating and rating <= 2 and any(word in lowered for word in ["great", "amazing", "perfect"]) else 0.0
    return min(1.0, cue_score + mismatch)

