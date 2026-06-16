from __future__ import annotations

from dataclasses import dataclass

from src.preprocessing.emoji_handler import replace_emojis
from src.preprocessing.language_identifier import identify_language
from src.preprocessing.normalizer import normalize_text
from src.preprocessing.spell_corrector import correct_common_misspellings


@dataclass(frozen=True)
class PreprocessedReview:
    original_text: str
    cleaned_text: str
    language: str


def preprocess_review(text: str) -> PreprocessedReview:
    with_emoji_text = replace_emojis(text or "")
    cleaned = correct_common_misspellings(normalize_text(with_emoji_text))
    return PreprocessedReview(original_text=text or "", cleaned_text=cleaned, language=identify_language(cleaned))

