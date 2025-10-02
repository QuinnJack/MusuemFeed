# Culture Museums Feed Microservice

This FastAPI project ingests museum news feeds, enriches them with mocked AI
summaries, and exposes a REST API that the WordPress plugin can consume.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

By default the service stores data in `data/museum_feed.db` (SQLite). Configure
settings through environment variables prefixed with `CM_` or by editing the
files in `config/`.

## Key endpoints

- `POST /ingest` — pull fresh content from the configured feeds and persist
  scored articles.
- `GET /articles` — fetch curated news filtered by region, topics, language, and
  minimum score. Mirrors the contract required by the Gutenberg blocks.
- `GET /health` — simple liveness probe for deployment targets.

## Tests

Install optional development dependencies and run `pytest` once tests are added
in future iterations.
