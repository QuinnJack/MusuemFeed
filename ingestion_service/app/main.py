"""FastAPI application entry point."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

from .config import FeedConfig, get_settings, load_feeds
from .database import init_db, session_scope
from .ingestion import deduplicate, ingest_feed
from .models import Article
from .scoring import score_article
from .schemas import ArticleResponse, PaginatedResponse

app = FastAPI(title="Culture Museums Feed Service", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/ingest")
def ingest(feeds: Optional[List[FeedConfig]] = None) -> dict:
    settings = get_settings()
    feed_configs = feeds or load_feeds(settings)
    if not feed_configs:
        raise HTTPException(status_code=400, detail="No feed configurations available")

    ingested_count = 0
    for feed in feed_configs:
        articles = ingest_feed(feed)
        with session_scope() as session:
            existing_ids = list(session.exec(select(Article.external_id)))
            new_articles = deduplicate(existing_ids, articles)
            for article in new_articles:
                score = score_article(article.title, article.summary, article.topics)
                if score < settings.min_relevance_score:
                    continue
                session.add(
                    Article(
                        external_id=article.external_id,
                        title=article.title,
                        body=article.body,
                        summary=article.summary,
                        source=article.source,
                        published_at=article.published_at,
                        region=article.region,
                        topics=article.topics,
                        image_url=article.image_url,
                        language=article.language,
                        canonical_url=article.canonical_url,
                        score=score,
                    )
                )
                ingested_count += 1
    return {"ingested": ingested_count}


@app.get("/articles", response_model=PaginatedResponse)
def list_articles(
    region: Optional[str] = None,
    topics: Optional[List[str]] = Query(default=None),
    count: int = Query(default=10, ge=1, le=50),
    language: Optional[str] = None,
    min_score: Optional[float] = None,
) -> PaginatedResponse:
    settings = get_settings()
    with session_scope() as session:
        statement = select(Article)
        if region:
            statement = statement.where(Article.region == region)
        if language:
            statement = statement.where(Article.language == language)
        statement = statement.order_by(Article.published_at.desc())
        results = session.exec(statement).all()

    min_score = min_score or settings.min_relevance_score
    filtered = [article for article in results if article.score >= min_score]
    if topics:
        topics_lower = {topic.lower() for topic in topics}
        filtered = [
            article
            for article in filtered
            if topics_lower.intersection({t.lower() for t in article.topics})
        ]
    limited = filtered[:count]
    items = [
        ArticleResponse(
            id=article.id,
            title=article.title,
            summary=article.summary,
            source=article.source,
            published_at=article.published_at,
            image_url=article.image_url,
            region=article.region,
            topics=article.topics,
            score=article.score,
            language=article.language,
            canonical_url=article.canonical_url,
            ai_generated_image=article.ai_generated_image,
        )
        for article in limited
    ]
    return PaginatedResponse(items=items, meta={"count": len(items)})


__all__ = ["app"]
