# HealthspanWire ©

HealthspanWire is a Jekyll-based publication focused on longevity science and healthspan research.

## AI indexing and retrieval surfaces

The project exposes multiple machine-readable endpoints to support search engines, AI crawlers, and retrieval systems:

- `/llms.txt` — concise AI-facing site descriptor.
- `/llms-full.txt` — expanded machine-readable article index.
- `/ai-index.json` — structured map of canonical sections and posts.
- `/search.json` — post search index for client-side and retrieval use.
- `/sitemap.xml` — canonical URL and recency map.
- `/robots.txt` — crawler directives and discoverability hints.
- `/ai-policy/` — usage and attribution expectations for AI systems.

## Content and metadata expectations

For strongest retrieval quality, posts should include (when available):

- `title`
- `date`
- `description`
- `author`
- `categories` / `tags`
- `topic`
- `signal_id`
- `source_url`

## Validation

Run metadata validation script:

```bash
python3 scripts/validate_signal_metadata.py
```
