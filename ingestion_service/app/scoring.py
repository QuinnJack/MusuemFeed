"""Simple relevance scoring helpers."""
from __future__ import annotations

from typing import Iterable


def score_article(title: str, summary: str, topics: Iterable[str]) -> float:
    """Return a naive relevance score.

    The implementation is intentionally simplistic but keeps the architecture
    ready for a more sophisticated ML model. The score is normalised between
    0.0 and 1.0.
    """

    base = 0.4 if title else 0.0
    base += 0.3 if summary else 0.0

    topic_bonus = min(len(list(topics)) * 0.05, 0.3)
    return min(base + topic_bonus, 1.0)


__all__ = ["score_article"]
