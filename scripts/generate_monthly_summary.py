import argparse
import datetime
import os
import re
from pathlib import Path

from openai import OpenAI

POSTS_DIR = Path("_posts")
SIGNALS_DATA_FILE = Path("_data/signals.yml")
MONTHLY_CATEGORY = "monthly-summary"
BASE_CATEGORY = "longevity"

SYSTEM_PROMPT = """You are a health journalist writing the monthly deep-dive for HealthspanWire, a longevity publication for curious adults who want to age well — people who follow health science but are not researchers or clinicians.

This report is a **full editorial article of approximately 1,500 words**. It translates the month's longevity research into a clear, honest narrative that helps readers understand what actually moved the needle — what was proven, what is still early, and what they should actually care about.

---

## Output Format and Structure

Use clean Markdown throughout. Follow this exact section order:

**Opening** (2–3 paragraphs, no header)
A plain-language opening that captures the month's defining theme. What was the most important thing that happened in longevity science this month, and why should a health-conscious person care? Be concrete and specific. No jargon in the opening paragraph.

---

**## What the science showed this month**
Cover the month's most significant research findings. For each major finding, explain: what was studied, who it was studied in (mice, a small group of people, a large trial), what the result was in plain terms, and what it might mean for someone trying to stay healthy longer. Hyperlink relevant claims to internal HealthspanWire links: [linked text](url). Use `###` subheadings where distinct topics warrant it. Aim for 250–300 words.

---

**## Food, movement, and daily habits**
Dedicated section for dietary research, nutritional compounds, fasting, exercise science, sleep, and lifestyle factors with evidence in healthspan or longevity. Name specific nutrients, doses, protocols, and populations studied — but explain them in plain English. Link claims to internal HealthspanWire articles/signals inline. Aim for 200–250 words.

---

**## What might change how we age**
Highlight the most significant treatments, therapies, or technologies that moved forward this month — drugs in trials, gene therapies, supplements gaining evidence. Use a blockquote (`>`) to call out the single most important development of the month. Explain what stage each is at and what realistic timeline for impact looks like. Aim for 150–200 words.

---

**## What this means for you**
Step back and connect the month's findings to real choices or awareness a health-focused adult would care about. What should readers take away — not as medical advice, but as informed context for decisions about their health, habits, or what to watch? Aim for 150–200 words.

---

**## Who is building what**
What does this month's activity reveal about where money and research energy are flowing in longevity science? Name companies, funders, or strategic moves where present in the sources — and explain briefly why it matters for when new treatments might become available. Aim for 100–150 words.

---

**## What to watch next month**
3–4 specific, grounded forward-looking observations based on trends visible in this month's data. Each should be a short paragraph. Be concrete — name the trial, the compound, or the question the science is about to answer.

---

## Formatting Standards

- Use `##` for main section headers, `###` for subsections within a section.
- **Bold** key terms, compound names, or findings on first mention — then define them inline in plain English.
- Use `>` blockquotes for the single most important finding of the month.
- Separate each major section with `---`.
- Hyperlink specific article titles or named claims to internal URLs provided in the input (`Internal Article`, optional `Signal Links`) inline.
- Write in full paragraphs. No bullet lists except sparingly in "What to watch."

## Editorial Standards

- Write at a 10th-grade reading level. Use "you" and "people" not "patients" or "subjects."
- Define any scientific term inline on first use (e.g. "senolytics — drugs that clear out old, damaged cells").
- Synthesize across sources — surface patterns and honest assessments rather than summarising articles one by one.
- Only draw on information present in the provided source summaries. Do not link out to external domains.
- Be honest about evidence quality: distinguish mouse studies from small human trials from large randomised trials.
- No hype, no speculation beyond what sources support.
- Avoid clichés: "science is advancing", "researchers are increasingly", "promising new research".
- Prefer active voice and concrete claims.
"""

USER_PROMPT_TEMPLATE = """Create the monthly industry report for {period}.

{article_summaries}
"""

MAX_INPUT_TOKENS = 24000
CHARS_PER_TOKEN_ESTIMATE = 4
MAX_SUMMARY_CHARS_PER_ARTICLE = 320


def yaml_escape(text: str) -> str:
    return (text or "").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def slugify(text: str) -> str:
    slug_raw = re.sub(r"\s+", "-", text.lower().strip())
    return "".join(c for c in slug_raw if c.isalnum() or c == "-").strip("-")


def parse_front_matter(content: str) -> tuple[dict, str]:
    if not content.startswith("---\n"):
        return {}, content

    end = content.find("\n---\n", 4)
    if end == -1:
        return {}, content

    fm_text = content[4:end]
    body = content[end + 5 :]
    fm = {}
    for line in fm_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip()
    return fm, body.strip()


def post_month_from_filename(path: Path) -> str | None:
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})-", path.name)
    if not match:
        return None
    return f"{match.group(1)}-{match.group(2)}"


def build_internal_post_url(path: Path) -> str:
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", path.name)
    if not match:
        return ""
    year, month, day, slug = match.groups()
    return f"/{year}/{month}/{day}/{slug}/"


def is_monthly_post(front_matter: dict) -> bool:
    categories = front_matter.get("categories", "")
    return MONTHLY_CATEGORY in categories


def collect_month_articles(period: str) -> list[dict]:
    rows = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        if post_month_from_filename(path) != period:
            continue

        content = path.read_text(encoding="utf-8")
        front_matter, body = parse_front_matter(content)

        if is_monthly_post(front_matter):
            continue

        title = front_matter.get("title", "").strip().strip('"')
        source_url = front_matter.get("source_url", "").strip().strip('"')
        publisher = front_matter.get("publisher", "").strip().strip('"')
        excerpt = front_matter.get("excerpt", "").strip().strip('"')

        summary_text = excerpt if excerpt else body[:500]
        signal_ids = parse_inline_list(front_matter.get("signal_ids", ""))
        signal_links = [f"/signals/#{signal_id}" for signal_id in signal_ids]
        if not title:
            continue

        rows.append(
            {
                "title": title,
                "publisher": publisher,
                "source_url": source_url,
                "internal_url": build_internal_post_url(path),
                "signal_links": signal_links,
                "summary": summary_text,
            }
        )
    return rows


def build_article_prompt_rows(articles: list[dict]) -> str:
    chunks = []
    for idx, article in enumerate(articles, start=1):
        summary = article["summary"].strip().replace("\n", " ")
        if len(summary) > MAX_SUMMARY_CHARS_PER_ARTICLE:
            summary = f"{summary[: MAX_SUMMARY_CHARS_PER_ARTICLE - 1].rstrip()}…"
        chunks.append(
            f"{idx}. Title: {article['title']}\n"
            f"Publisher: {article['publisher'] or 'Unknown'}\n"
            f"Internal Article: {article['internal_url'] or 'N/A'}\n"
            f"Source (reference only): {article['source_url'] or 'N/A'}\n"
            f"Signal Links: {', '.join(article['signal_links']) if article['signal_links'] else 'N/A'}\n"
            f"Summary: {summary}\n"
        )
    return "\n".join(chunks)


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // CHARS_PER_TOKEN_ESTIMATE)


def prune_articles_to_token_budget(period: str, articles: list[dict]) -> tuple[list[dict], bool]:
    selected: list[dict] = []
    truncated = False
    for article in articles:
        candidate = [*selected, article]
        prompt = USER_PROMPT_TEMPLATE.format(period=period, article_summaries=build_article_prompt_rows(candidate))
        total_estimated = estimate_tokens(SYSTEM_PROMPT) + estimate_tokens(prompt)
        if total_estimated > MAX_INPUT_TOKENS:
            truncated = True
            break
        selected.append(article)

    return (selected if selected else articles[:1], truncated)


def parse_inline_list(value: str) -> list[str]:
    cleaned = (value or "").strip()
    if not cleaned.startswith("[") or not cleaned.endswith("]"):
        return []
    inner = cleaned[1:-1].strip()
    if not inner:
        return []
    return [item.strip().strip('"').strip("'") for item in inner.split(",") if item.strip()]


def load_signal_titles() -> dict[str, str]:
    if not SIGNALS_DATA_FILE.exists():
        return {}

    current_id = None
    title_by_id: dict[str, str] = {}
    for raw in SIGNALS_DATA_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- id:"):
            current_id = line.split(":", 1)[1].strip().strip('"').strip("'")
            continue
        if current_id and line.startswith("title:"):
            title_by_id[current_id] = line.split(":", 1)[1].strip().strip('"').strip("'")
            current_id = None
    return title_by_id


def collect_signal_updates(period: str) -> dict[str, dict[str, int]]:
    updates: dict[str, dict[str, int]] = {}
    for path in sorted(POSTS_DIR.glob("*.md")):
        if post_month_from_filename(path) != period:
            continue

        content = path.read_text(encoding="utf-8")
        front_matter, _ = parse_front_matter(content)
        if is_monthly_post(front_matter):
            continue

        signal_ids = parse_inline_list(front_matter.get("signal_ids", ""))
        if not signal_ids:
            continue

        stance = front_matter.get("signal_stance", "mentions").strip().strip('"').strip("'")
        if stance not in {"supports", "contradicts", "mixed", "mentions"}:
            stance = "mentions"

        for signal_id in signal_ids:
            updates.setdefault(signal_id, {"supports": 0, "contradicts": 0, "mixed": 0, "mentions": 0})
            updates[signal_id][stance] += 1
    return updates


def build_signal_updates_section(period: str) -> str:
    updates = collect_signal_updates(period)
    if not updates:
        return ""

    titles = load_signal_titles()
    lines = ["## Signal Tracker Updates", ""]
    for signal_id in sorted(updates.keys()):
        counts = updates[signal_id]
        label = titles.get(signal_id, signal_id)
        total = sum(counts.values())
        lines.append(
            f"- **{label}** (`{signal_id}`): {total} linked post(s) "
            f"(supports: {counts['supports']}, contradicts: {counts['contradicts']}, "
            f"mixed: {counts['mixed']}, mentions: {counts['mentions']})."
        )
    return "\n".join(lines)


def monthly_post_exists(period: str) -> bool:
    for path in POSTS_DIR.glob(f"{period}-*.md"):
        content = path.read_text(encoding="utf-8")
        front_matter, _ = parse_front_matter(content)
        if is_monthly_post(front_matter) and front_matter.get("period", "").strip('"') == period:
            return True
    return False


def write_monthly_post(period: str, article_count: int, content: str) -> Path:
    year, month = period.split("-")
    month_name = datetime.date(int(year), int(month), 1).strftime("%B")
    title = f"Monthly Report: {month_name} {year}"
    slug = slugify(f"monthly-report-{month_name}-{year}")
    post_date = datetime.date(int(year), int(month), 1) + datetime.timedelta(days=27)
    while post_date.month != int(month):
        post_date -= datetime.timedelta(days=1)

    date_prefix = post_date.isoformat()
    filename = POSTS_DIR / f"{date_prefix}-{slug}.md"
    suffix = 1
    while filename.exists():
        filename = POSTS_DIR / f"{date_prefix}-{slug}-{suffix}.md"
        suffix += 1

    safe_title = yaml_escape(title)
    safe_excerpt = yaml_escape(f"A monthly roundup for {month_name} {year} based on {article_count} articles")

    md = f"""---
title: \"{safe_title}\"
date: {post_date.isoformat()}T09:00:00Z
layout: post
categories: [{MONTHLY_CATEGORY}]
tags: [monthly, roundup, longevity, healthspan]
excerpt: \"{safe_excerpt}.\"
period: \"{period}\"
source_count: {article_count}
---

{content}
"""
    filename.write_text(md, encoding="utf-8")
    return filename


def get_default_period() -> str:
    today = datetime.date.today().replace(day=1)
    last_month_end = today - datetime.timedelta(days=1)
    return last_month_end.strftime("%Y-%m")


def generate_monthly_summary(period: str, force: bool = False) -> Path | None:
    if not POSTS_DIR.exists():
        raise FileNotFoundError("_posts directory does not exist")

    if monthly_post_exists(period) and not force:
        print(f"Monthly report already exists for {period}. Use --force to generate another.")
        return None

    articles = collect_month_articles(period)
    if not articles:
        print(f"No articles found for {period}.")
        return None
    articles, truncated = prune_articles_to_token_budget(period, articles)
    if truncated:
        print(
            f"Prompt input exceeded token budget; summarizing top {len(articles)} articles "
            f"for {period} to avoid request-size rate limits."
        )

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    article_summaries = build_article_prompt_rows(articles)
    user_prompt = USER_PROMPT_TEMPLATE.format(period=period, article_summaries=article_summaries)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1800,
        temperature=0.4,
    )
    monthly_content = response.choices[0].message.content.strip()
    signal_updates_section = build_signal_updates_section(period)
    if signal_updates_section:
        monthly_content = f"{monthly_content}\n\n{signal_updates_section}"
    out_file = write_monthly_post(period, len(articles), monthly_content)
    print(f"Created monthly report: {out_file}")
    return out_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate monthly summary posts from existing daily posts.")
    parser.add_argument("--month", default=get_default_period(), help="Month to summarize in YYYY-MM format")
    parser.add_argument("--force", action="store_true", help="Generate even if a monthly post already exists")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not re.match(r"^\d{4}-\d{2}$", args.month):
        raise ValueError("--month must be in YYYY-MM format")
    generate_monthly_summary(args.month, force=args.force)
