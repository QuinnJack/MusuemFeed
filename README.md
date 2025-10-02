# Culture Museums Feed Platform

This repository contains the skeleton for the Culture Museums news aggregation
platform. It is organised as a FastAPI ingestion microservice and a reusable
WordPress plugin that renders curated layouts through Gutenberg blocks.

## Project structure

```
.
├── config/                     # Feed presets per region (JSON)
├── ingestion_service/          # FastAPI microservice for ingestion
├── wp-plugin/                  # WordPress plugin implementation
├── data/                       # SQLite database location (gitignored)
└── README.md                   # You are here
```

## Getting started

1. **Ingestion service**

   ```bash
   cd ingestion_service
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   uvicorn app.main:app --reload
   ```

   Trigger an ingestion run once the service is running:

   ```bash
   http POST http://localhost:8000/ingest
   ```

   Fetch curated articles:

   ```bash
   http "http://localhost:8000/articles?region=canada&count=6&layout=grid"
   ```

2. **WordPress plugin**

   - Copy `wp-plugin/culture-museums-news` into `wp-content/plugins/` and
     activate it.
   - Configure the ingestion API endpoint under **Settings → Culture Museums
     News**.
   - Insert the **Museum News Grid** block on a landing page to render content
     from the microservice.

## Delivery roadmap

The repository mirrors the multi-week delivery plan:

- **Week 0** – Repository skeleton, environment configuration, architecture
  documentation (completed here).
- **Week 1** – Feed ingestion from three Canadian museums, persistence, and the
  `/articles` API (implemented as FastAPI endpoints with SQLite storage).
- **Week 2** – Deduplication, naive relevance scoring, and mocked EN/FR
  summarisation utilities.
- **Week 3** – Image extraction from feeds plus placeholders for Unsplash/Pexels
  fallbacks.
- **Week 4** – WordPress plugin skeleton with CPT, REST proxy, and a Gutenberg
  block matching the existing landing page layout.
- **Week 5** – Admin settings page scaffolding for region presets and ingestion
  thresholds; caching handled via WordPress transients.
- **Week 6** – End-to-end integration via shared API contract and deployment
  notes added to the documentation.

Future iterations can iterate on AI-powered rewriting, advanced image fallbacks,
and staging deployment automation.
