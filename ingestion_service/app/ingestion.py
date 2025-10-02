"""Feed ingestion utilities."""
from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Iterable, List, Sequence

import feedparser

from .config import FeedConfig
from .summarisation import summarise


class IngestedArticle:
    """Lightweight representation of an ingested article."""

    def __init__(
        self,
        *,
        external_id: str,
        title: str,
        body: str,
        summary: str,
        source: str,
        published_at: datetime,
        region: str,
        topics: Sequence[str],
        image_url: str | None,
        language: str,
        canonical_url: str | None,
    ) -> None:
        self.external_id = external_id
        self.title = title
        self.body = body
        self.summary = summary
        self.source = source
        self.published_at = published_at
        self.region = region
        self.topics = list(topics)
        self.image_url = image_url
        self.language = language
        self.canonical_url = canonical_url

    def as_dict(self) -> dict:
        return {
            "external_id": self.external_id,
            "title": self.title,
            "body": self.body,
            "summary": self.summary,
            "source": self.source,
            "published_at": self.published_at,
            "region": self.region,
            "topics": self.topics,
            "image_url": self.image_url,
            "language": self.language,
            "canonical_url": self.canonical_url,
        }


def _hash_entry(entry: feedparser.FeedParserDict) -> str:
    base = entry.get("id") or entry.get("link") or entry.get("title", "")
    if not base:
        base = str(entry)
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def _parse_datetime(entry: feedparser.FeedParserDict) -> datetime:
    published = entry.get("published_parsed")
    if published:
        return datetime(*published[:6])
    return datetime.utcnow()


def ingest_feed(feed: FeedConfig) -> List[IngestedArticle]:
    """Fetch articles from a feed configuration."""

    parsed = feedparser.parse(feed.url)
    articles: List[IngestedArticle] = []
    for entry in parsed.entries:
        external_id = _hash_entry(entry)
        title = entry.get("title", "Untitled")
        summary = entry.get("summary", "")
        body = entry.get("content", [{}])[0].get("value", summary)
        language = entry.get("language", feed.language)
        published_at = _parse_datetime(entry)
        canonical_url = entry.get("link")
        image_url = None
        media = entry.get("media_content") or entry.get("links", [])
        for media_entry in media:
            href = media_entry.get("url") or media_entry.get("href")
            if href and any(href.lower().endswith(ext) for ext in (".jpg", ".png", ".jpeg")):
                image_url = href
                break

        summary_text = summarise(summary or body, hints=[feed.summary_hint] if feed.summary_hint else None, language=language)
        articles.append(
            IngestedArticle(
                external_id=external_id,
                title=title,
                body=body,
                summary=summary_text,
                source=feed.name,
                published_at=published_at,
                region=feed.region,
                topics=feed.topics,
                image_url=image_url,
                language=language,
                canonical_url=canonical_url,
            )
        )
    return articles


def deduplicate(existing_ids: Iterable[str], articles: Iterable[IngestedArticle]) -> List[IngestedArticle]:
    """Filter out articles that already exist."""

    known = set(existing_ids)
    unique: List[IngestedArticle] = []
    for article in articles:
        if article.external_id in known:
            continue
        known.add(article.external_id)
        unique.append(article)
    return unique


__all__ = ["ingest_feed", "deduplicate", "IngestedArticle"]
