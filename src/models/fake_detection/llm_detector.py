from __future__ import annotations

LLM_MARKERS = {
    "as an ai",
    "overall, i would say",
    "in conclusion",
    "it is worth noting",
    "this product offers a delightful",
}


def llm_generated_score(text: str) -> float:
    lowered = (text or "").lower()
    marker_hits = sum(1 for marker in LLM_MARKERS if marker in lowered)
    words = lowered.split()
    diversity = len(set(words)) / max(1, len(words))
    repetitive_penalty = 0.25 if len(words) > 35 and diversity < 0.45 else 0.0
    return min(1.0, marker_hits * 0.35 + repetitive_penalty)

