"""Pydantic schemas for the API."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ArticleResponse(BaseModel):
    id: int
    title: str
    summary: str
    source: str
    published_at: datetime
    image_url: Optional[str]
    region: str
    topics: List[str]
    score: float
    language: str
    canonical_url: Optional[str]
    ai_generated_image: bool


class PaginatedResponse(BaseModel):
    items: List[ArticleResponse]
    meta: dict


__all__ = ["ArticleResponse", "PaginatedResponse"]
