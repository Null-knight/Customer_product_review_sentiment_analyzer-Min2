from __future__ import annotations

import math
import re


def linguistic_features(text: str) -> dict[str, float]:
    words = re.findall(r"[a-zA-Z]+", text or "")
    unique_words = set(words)
    word_count = len(words)
    char_count = len(text or "")
    avg_word_len = sum(len(word) for word in words) / word_count if word_count else 0
    lexical_diversity = len(unique_words) / word_count if word_count else 0
    entropy = 0.0
    if word_count:
        for word in unique_words:
            p = words.count(word) / word_count
            entropy -= p * math.log2(p)
    return {
        "word_count": float(word_count),
        "char_count": float(char_count),
        "avg_word_len": round(avg_word_len, 3),
        "lexical_diversity": round(lexical_diversity, 3),
        "word_entropy": round(entropy, 3),
        "exclamation_count": float((text or "").count("!")),
        "question_count": float((text or "").count("?")),
    }

