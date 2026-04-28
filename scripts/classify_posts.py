#!/usr/bin/env python3
"""
Batch-classify all existing posts with explicit topic and impact front matter fields.
Pure keyword-based, no API calls. Run from the repo root: python scripts/classify_posts.py
"""
import re
import sys
from pathlib import Path

POSTS_DIR = Path("_posts")

# Signal ID → primary topic
SIGNAL_TOPIC = {
    "senolytic-clinical-validation": "therapeutics",
    "rapamycin-healthspan-extension": "therapeutics",
    "caloric-restriction-mimetics": "nutrition",
    "gut-microbiome-aging": "nutrition",
    "creatine-healthspan-effects": "nutrition",
    "sex-healthspan-lifespan": "nutrition",
    "epigenetic-clock-adoption": "biomarkers",
    "blood-biomarker-panels": "biomarkers",
    "ai-drug-discovery-aging": "technology",
    "gene-therapy-aging": "technology",
    "longevity-regulatory-frameworks": "policy",
    "longevity-funding-surge": "policy",
}

# Keyword rules in priority order (most specific first to avoid over-matching)
TOPIC_KEYWORD_RULES = [
    ("technology", [
        "gene therapy", "crispr", "gene edit", "machine learning", "artificial intelligence",
        "reprogramming", "yamanaka", "telomerase", "computational biology", "in silico",
        "alphafold", "wearable sensor", "whole genome", "genomic sequencing",
        "epigenetic reprogramm", "partial reprogramm", "aav vector", "lentiviral",
        "rna therapy", "mrna", "base edit", "digital twin", "ai-powered", "ai model",
        "deep learning", "neural network", "large language model", "biotech ai",
        "genome editing", "genetic engineering", "cell reprogramming", "gene expression",
    ]),
    ("biomarkers", [
        "epigenetic clock", "biological age", "dna methylation", "methylation clock",
        "proteomics", "metabolomics", "blood panel", "grimage", "dunedinpace",
        "horvath clock", "aging clock", "liquid biopsy", "plasma protein",
        "biological aging marker", "phenotypic age", "biologic age",
        "biomarker", "blood marker", "cognitive decline", "brain aging", "tau",
        "amyloid", "cognitive assessment", "cognitive test", "brain scan",
        "ldl cholesterol", "hdl cholesterol", "blood pressure", "vascular aging",
        "cardiac biomarker", "inflammation marker", "crp", "il-6", "inflammaging",
    ]),
    ("policy", [
        "fda approved", "fda approval", "approved by fda", "ema approval",
        "regulatory approval", "venture capital", "series a", "series b",
        "clinical development timeline", "reimbursement", "nih grant",
        "longevity funding", "longevity investment", "biotech funding",
        "clinical authorization", "market authorization", "drug approval",
        "ce mark", "clinical pathway", "regulatory framework", "patent",
        "ipo", "merger", "acquisition", "company", "startup", "pharma company",
        "biotech", "licensed", "commercialization", "clinical program",
    ]),
    ("therapeutics", [
        "senolytic", "rapamycin", "rapalog", "nad+", "nmn", "nicotinamide riboside",
        "dasatinib", "quercetin", "fisetin", "metformin", "spermidine",
        "drug candidate", "longevity drug", "anti-aging drug", "senomorphic",
        "mtor inhibitor", "phase 2 trial", "phase 3 trial", "clinical trial",
        "randomized trial", "drug treatment", "therapeutic target", "compound",
        "stem cell therapy", "plasmapheresis", "young plasma", "blood dilution",
        "alzheimer drug", "dementia drug", "semaglutide", "ozempic", "glp-1",
        "tirzepatide", "mounjaro", "wegovy", "medication", "pharmaceutical",
        "immunotherapy", "cancer therapy", "hormone therapy", "testosterone",
        "estrogen therapy", "hrt", "hormone replacement", "supplement trial",
        "drug trial", "treatment trial", "clinical study", "double-blind",
    ]),
    ("nutrition", [
        "intermittent fasting", "time-restricted eating", "caloric restriction",
        "calorie restriction", "microbiome", "gut bacteria", "gut microbiota",
        "dietary intervention", "plant-based", "mediterranean diet", "omega-3",
        "protein intake", "muscle mass", "strength training", "zone 2",
        "cardiovascular exercise", "physical activity", "sleep quality",
        "creatine", "diet", "nutrition", "food", "eating", "fasting",
        "exercise", "lifestyle", "probiotic", "prebiotic", "fiber intake",
        "heart health", "cardiovascular", "blood sugar", "insulin", "metabolic",
        "obesity", "weight loss", "body weight", "bmi", "sarcopenia",
        "muscle strength", "aerobic fitness", "vo2 max", "sleep", "stress",
        "meditation", "alcohol", "smoking", "ultraprocessed", "processed food",
    ]),
]

# Publishers whose content is typically press releases / announcements
PRESS_RELEASE_PUBLISHERS = {
    "globenewswire.com", "prnewswire.com", "businesswire.com", "accesswire.com",
}

# Impact classification phrase lists
LANDMARK_PHRASES = [
    "fda approved", "fda approval", "approved by fda", "phase 3", "phase iii",
    "pivotal trial", "landmark study", "approval granted", "marketing authorization",
]
SIGNIFICANT_PHRASES = [
    "clinical trial", "human trial", "randomized", "placebo-controlled", "double-blind",
    "published in", "new england journal", "nejm", "nature aging", "cell metabolism",
    "jama", "lancet", "science advances", "human study", "participants", "subjects",
    "adults aged", "older adults", "peer-reviewed", "published study",
    "patients", "men and women", "women and men", "cohort study",
    "observational study", "longitudinal study", "cross-sectional",
]
NOTEWORTHY_PHRASES = [
    "meta-analysis", "systematic review", "review finds", "mouse study", "animal study",
    "preclinical", "pre-clinical", "laboratory study", "in vitro", "in vivo",
    "conference", "preliminary", "pilot study",
]


def parse_front_matter(content: str):
    if not content.startswith("---\n"):
        return None, content
    end = content.find("\n---\n", 4)
    if end == -1:
        return None, content
    return content[4:end], content[end + 5:]


def get_field(fm: str, field: str) -> str:
    m = re.search(rf"^{field}:\s*(.+)$", fm, re.MULTILINE)
    return m.group(1).strip() if m else ""


def has_field(fm: str, field: str) -> bool:
    return bool(re.search(rf"^{field}:", fm, re.MULTILINE))


def infer_topic(title: str, body_text: str, signal_ids_str: str) -> str:
    # Signal-based assignment takes priority
    for sid in re.split(r"[\s,\[\]]+", signal_ids_str):
        sid = sid.strip()
        if sid in SIGNAL_TOPIC:
            return SIGNAL_TOPIC[sid]

    # Use title + full body text for richer keyword matching
    text = (title + " " + body_text).lower()
    for topic, keywords in TOPIC_KEYWORD_RULES:
        if any(kw in text for kw in keywords):
            return topic
    return ""


def infer_impact(
    title: str,
    body_text: str,
    publisher: str,
    signal_confidence: str,
    signal_stance: str,
    signal_ids_str: str,
) -> str:
    pub = publisher.lower().strip('"\'')
    if any(p in pub for p in PRESS_RELEASE_PUBLISHERS):
        return "general"

    text = (title + " " + body_text).lower()

    if any(p in text for p in LANDMARK_PHRASES):
        return "landmark"

    has_signals = bool(re.search(r"[a-z]", signal_ids_str.strip().strip("[]")))
    if signal_confidence == "medium" and has_signals and signal_stance == "supports":
        return "landmark"

    if any(p in text for p in SIGNIFICANT_PHRASES):
        return "significant"
    if has_signals or signal_confidence in ("medium", "high"):
        return "noteworthy"
    if any(p in text for p in NOTEWORTHY_PHRASES):
        return "noteworthy"

    return "general"


def classify_post(path: Path) -> tuple[bool, str]:
    content = path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(content)
    if fm is None:
        return False, "no front matter"

    already_topic = has_field(fm, "topic")
    already_impact = has_field(fm, "impact")
    if already_topic and already_impact:
        return False, "already classified"

    title = get_field(fm, "title").strip("\"'")
    excerpt = get_field(fm, "excerpt").strip("\"'")
    signal_ids_str = get_field(fm, "signal_ids")
    publisher = get_field(fm, "publisher")
    signal_confidence = get_field(fm, "signal_confidence")
    signal_stance = get_field(fm, "signal_stance")

    # Use the full post body (gist text) for richer keyword matching
    body_text = excerpt + " " + body[:2000]

    new_lines = []
    if not already_topic:
        topic = infer_topic(title, body_text, signal_ids_str)
        if topic:
            new_lines.append(f'topic: "{topic}"')

    if not already_impact:
        impact = infer_impact(title, body_text, publisher, signal_confidence, signal_stance, signal_ids_str)
        new_lines.append(f'impact: "{impact}"')

    if not new_lines:
        return False, "nothing to add"

    new_fm = fm.rstrip() + "\n" + "\n".join(new_lines)
    path.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")
    return True, ", ".join(new_lines)


def main():
    posts = sorted(POSTS_DIR.glob("*.md"))
    if not posts:
        print(f"No posts found in {POSTS_DIR}. Run from repo root.")
        sys.exit(1)

    modified = 0
    skipped = 0
    errors = 0
    topic_counts: dict[str, int] = {}
    impact_counts: dict[str, int] = {}

    for post in posts:
        try:
            changed, detail = classify_post(post)
            if changed:
                modified += 1
                # Track what was assigned (parse from detail string)
                for part in detail.split(", "):
                    if part.startswith('topic: "'):
                        t = part[8:].strip('"')
                        topic_counts[t] = topic_counts.get(t, 0) + 1
                    elif part.startswith('impact: "'):
                        i = part[9:].strip('"')
                        impact_counts[i] = impact_counts.get(i, 0) + 1
            else:
                skipped += 1
        except Exception as exc:
            print(f"  ERROR {post.name}: {exc}")
            errors += 1

    print(f"\nDone: {modified} modified, {skipped} skipped, {errors} errors / {len(posts)} total")
    if topic_counts:
        print("\nTopic assignments:")
        for t, n in sorted(topic_counts.items(), key=lambda x: -x[1]):
            print(f"  {t:20s} {n}")
    if impact_counts:
        print("\nImpact assignments:")
        for i, n in sorted(impact_counts.items(), key=lambda x: -x[1]):
            print(f"  {i:20s} {n}")


if __name__ == "__main__":
    main()
