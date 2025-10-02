"""Mock AI summarisation helpers."""
from __future__ import annotations

from textwrap import shorten
from typing import Iterable


def summarise(body: str, hints: Iterable[str] | None = None, language: str = "en") -> str:
    """Return a deterministic short summary of the body.

    The function mocks a call to an external AI service while ensuring that the
    resulting text is copyright safe by only working on the provided body.
    """

    hints_text = f" {' '.join(hints)}" if hints else ""
    summary = shorten(body.strip().replace("\n", " ") + hints_text, width=280, placeholder="…")
    if language == "fr":
        return f"[FR] {summary}"
    return summary


__all__ = ["summarise"]
