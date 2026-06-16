from __future__ import annotations


class InMemoryVectorStore:
    """Small local stand-in for FAISS-style similarity search."""

    def __init__(self) -> None:
        self.texts: list[str] = []

    def add(self, text: str) -> None:
        self.texts.append(text)

    def recent_texts(self, limit: int = 1000) -> list[str]:
        return self.texts[-limit:]

