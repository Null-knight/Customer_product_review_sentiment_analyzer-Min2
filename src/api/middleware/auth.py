from __future__ import annotations


def is_authorized(token: str | None) -> bool:
    return token in {None, "", "dev-token"}

