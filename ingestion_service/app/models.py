"""Database models for the ingestion microservice."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
from sqlmodel import Field, SQLModel


def default_topics() -> List[str]:
    """Return a mutable default list for topics."""

    return []


class Article(SQLModel, table=True):
    """Stored news article metadata."""

    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(index=True, unique=True)
    title: str
    body: str
    summary: str
    source: str
    published_at: datetime
    region: str = Field(index=True)
    topics: List[str] = Field(default_factory=default_topics, sa_column=Column(JSON))
    image_url: Optional[str] = None
    score: float = Field(default=0.0, index=True)
    language: str = Field(default="en")
    canonical_url: Optional[str] = None
    ai_generated_image: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )


__all__ = ["Article"]
