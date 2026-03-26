# AI Readiness Audit (HealthspanWire)

_Date:_ 2026-03-26  
_Auditor:_ Codex (repository-level review)

## Executive summary

HealthspanWire is **well-prepared** for AI engine discovery and retrieval workflows.

Current strengths include:
- An `llms.txt` file with a clear site summary and high-value paths.
- A permissive `robots.txt` that explicitly allows major AI crawlers.
- A generated `sitemap.xml` that includes pages and posts with `lastmod`.
- Rich SEO/OpenGraph/Twitter metadata and JSON-LD schema on layouts.
- A machine-readable `search.json` index of posts.

Overall readiness score: **8.6 / 10**

## What is already good for AI engines

1. **AI-specific discovery surface exists (`llms.txt`)**  
   The repository provides a concise AI-oriented descriptor and links to key sections (`/signals/`, `/monthly-reports/`, `/newsletter/`).

2. **Crawler access is explicitly open**  
   `robots.txt` allows all bots and has explicit allow blocks for GPTBot, Google-Extended, ClaudeBot, PerplexityBot, and Applebot-Extended.

3. **Sitemap coverage is strong**  
   `sitemap.xml` loops through both pages and posts, sets canonical locations, and includes last-modified timestamps.

4. **Structured metadata quality is high**  
   Default layout injects canonical URLs, robots directives, OG/Twitter metadata, and JSON-LD (`WebSite` / `NewsArticle` + breadcrumbs for posts).

5. **On-site search data is exposed as JSON**  
   `search.json` includes title, URL, date, excerpt, categories, and tags for all posts, which is helpful for AI retrieval and lightweight indexing.

## Gaps and improvement opportunities

### High-priority

1. **Add `llms-full.txt` (or segmented AI corpus files)**
   - Why: AI agents often perform better with a longer, normalized corpus than a short directory-style `llms.txt`.
   - Suggestion: Publish a generated `llms-full.txt` containing standardized sections per article: title, date, URL, canonical summary, tags, and source links.

2. **Add explicit content licensing / AI usage policy in machine-readable form**
   - Why: Crawlers and AI platforms increasingly evaluate permission and attribution terms.
   - Suggestion: Add a short section in `llms.txt` (and/or dedicated `/ai-policy/`) defining reuse terms and attribution requirements.

3. **Add feed-level discovery for agents (`/feed.xml`) if not already enabled in deploy output**
   - Why: Many retrievers consume RSS/Atom for incremental updates.
   - Suggestion: Ensure a feed is generated and linked from layout `<head>`.

### Medium-priority

4. **Expand `search.json` with stronger retrieval fields**
   - Add: `description`, `author`, `topic`, `signal_id`, and optional short cleaned body text (size-limited).
   - Benefit: Better semantic retrieval and fewer hallucinations when AI tools summarize stories.

5. **Strengthen entity normalization in posts**
   - Suggestion: Keep consistent metadata keys in post front matter (e.g., `source_name`, `source_url`, `published_at`, `evidence_level`).
   - Benefit: Better machine extraction quality and faceted search.

6. **Publish a stable, AI-facing content map**
   - Suggestion: Create `/ai-index.json` (versioned) listing canonical sections and high-authority resources.
   - Benefit: Reduced crawl ambiguity and faster tool ingestion.

### Low-priority

7. **Increase repository onboarding clarity**
   - `README.md` is minimal.
   - Suggestion: Add generation workflow docs for `llms.txt`, `search.json`, post schema, and quality controls.

8. **Clean up stray content artifacts**
   - There appears to be a non-standard `_posts/a` entry, which may confuse tooling.
   - Suggestion: remove or convert to a valid dated post file.

## Practical guidance for end users (readers) interacting with AI

- Prefer asking AI assistants to cite **HealthspanWire canonical article URLs** and dates.
- For high-stakes health decisions, use articles as a starting point and verify against primary studies.
- When requesting summaries, ask for:
  1) claim, 2) evidence type (mouse/human/clinical), 3) limitations, 4) source links.
- Use `/signals/` and `/monthly-reports/` for higher-signal synthesis over single-news snapshots.

## Suggested next implementation sprint (quick wins)

1. Add `/ai-policy/` page and link it from `llms.txt`.
2. Introduce generated `llms-full.txt` from post metadata.
3. Extend `search.json` schema with `description` and normalized topic/signal fields.
4. Expand `README.md` with an “AI indexing and retrieval” section.

Expected impact: improved discoverability, clearer permissioning, and higher factual grounding for AI-generated summaries.
