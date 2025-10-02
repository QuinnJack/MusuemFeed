# Culture Museums News Hub (WordPress Plugin)

This plugin registers the `cm_news_item` custom post type, exposes a REST
endpoint for museum news, and provides Gutenberg blocks that render curated
layouts fed by the ingestion microservice.

## Setup

1. Copy the `culture-museums-news` directory into your WordPress installation's
   `wp-content/plugins/` folder.
2. Install dependencies for the block editor bundle (placeholder `build/index.js`).
   Replace this file with the compiled assets from the block development
   pipeline.
3. Activate the plugin from the WordPress admin dashboard.
4. Configure the ingestion API URL and region presets under **Settings → Culture
   Museums News**.

## REST API

`GET /wp-json/cm/v1/news` matches the frontend contract defined by the
microservice. Parameters such as `region`, `topics`, `layout`, `count`, and
`language` are passed through to the ingestion service.

## Blocks

- **News Grid** (`cmn/news-grid`) — renders a responsive grid layout using the
  API contract shared with the ingestion microservice. Additional layouts (e.g.
  "big-main + 2 small") can be added by registering new block types following
  the same pattern.

## Roadmap

- Integrate dynamic block editor assets compiled with `@wordpress/scripts`.
- Add admin tools for mapping feeds to Gutenberg layout presets per region.
- Extend REST responses with caching headers for CDN friendliness.
