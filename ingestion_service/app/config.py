"""Application configuration utilities."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, BaseSettings, Field, validator


class FeedConfig(BaseModel):
    """Configuration for a single feed source."""

    name: str
    url: str
    region: str = Field(..., description="Region identifier, e.g. 'canada'.")
    topics: List[str] = Field(default_factory=list)
    language: str = Field("en", description="ISO language code")
    summary_hint: str | None = Field(
        default=None,
        description="Optional hint text used by the summarisation mock.",
    )


class Settings(BaseSettings):
    """Environment aware application settings."""

    database_url: str = Field(
        "sqlite:///./data/museum_feed.db",
        description="SQLAlchemy connection string for the article store.",
    )
    feeds_file: Path = Field(
        Path("config/feeds.canada.json"),
        description="Path to the JSON file that lists feed sources.",
    )
    summarisation_language_priority: List[str] = Field(
        default_factory=lambda: ["en", "fr"],
        description="Preferred languages for mocked summaries.",
    )
    min_relevance_score: float = Field(
        0.6, description="Default minimum relevance score for published articles."
    )

    class Config:
        env_prefix = "CM_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("feeds_file", pre=True)
    def _expand_path(cls, value: Any) -> Path:  # noqa: N805 - pydantic validator
        if isinstance(value, Path):
            return value
        return Path(value).expanduser().resolve()


@lru_cache()
def get_settings() -> Settings:
    """Return the cached settings instance."""

    return Settings()


def load_feeds(settings: Settings | None = None) -> List[FeedConfig]:
    """Load feed definitions from the configured JSON file."""

    import json

    settings = settings or get_settings()
    if not settings.feeds_file.exists():
        return []

    with settings.feeds_file.open("r", encoding="utf-8") as handle:
        raw: List[Dict[str, Any]] = json.load(handle)
    return [FeedConfig(**entry) for entry in raw]


__all__ = ["FeedConfig", "Settings", "get_settings", "load_feeds"]
