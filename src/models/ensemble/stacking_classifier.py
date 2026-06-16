from __future__ import annotations


def final_verdict(fake_score: float, spam_score: float, quality_score: float) -> dict:
    if fake_score >= 0.75:
        decision = "BLOCK"
    elif fake_score >= 0.55 or spam_score >= 0.55 or quality_score < 0.20:
        decision = "REVIEW"
    else:
        decision = "APPROVE"
    return {
        "decision": decision,
        "legit_probability": round(1 - max(fake_score, spam_score), 3),
        "reason": _reason(decision, fake_score, spam_score, quality_score),
    }


def _reason(decision: str, fake_score: float, spam_score: float, quality_score: float) -> str:
    if decision == "BLOCK":
        return "High fake-review probability"
    if spam_score >= 0.55:
        return "Promotional or off-topic spam risk"
    if fake_score >= 0.55:
        return "Moderate fake-review risk"
    if quality_score < 0.20:
        return "Low review quality"
    return "Review appears acceptable"

