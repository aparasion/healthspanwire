---
layout: default
title: All Articles
nav_title: Articles
permalink: /articles/
nav: true
nav_order: 1
description: "Browse all longevity and healthspan articles — filter by topic, impact, source, and date."
---

<section class="topics-hero">
  <h1>All Articles</h1>
  <p class="topics-subtitle">Browse all articles — filter by topic, how strong the science is, or date.</p>
</section>

{% comment %}
  Define signal IDs and keywords for each topic.
  We compute topic assignments at build time and store as data-topics attribute.
{% endcomment %}

{% assign therapeutics_signals = "senolytic-clinical-validation,rapamycin-healthspan-extension" | split: "," %}
{% assign therapeutics_keywords = "senolytic,rapamycin,dasatinib,quercetin,fisetin,anti-aging drug,longevity therapeutic,age-related disease,clinical trial,drug candidate" | split: "," %}

{% assign biomarkers_signals = "epigenetic-clock-adoption,blood-biomarker-panels" | split: "," %}
{% assign biomarkers_keywords = "epigenetic clock,biological age,dna methylation,horvath,grimace,dunedinpace,biomarker,proteomics,metabolomics,aging clock" | split: "," %}

{% assign nutrition_signals = "caloric-restriction-mimetics,gut-microbiome-aging" | split: "," %}
{% assign nutrition_keywords = "caloric restriction,intermittent fasting,nad+,nmn,nicotinamide,spermidine,microbiome,diet,nutrition,metformin,resveratrol" | split: "," %}

{% assign tech_signals = "ai-drug-discovery-aging,gene-therapy-aging" | split: "," %}
{% assign tech_keywords = "gene therapy,crispr,ai drug discovery,machine learning,yamanaka,telomerase,reprogramming,computational biology,wearable" | split: "," %}

{% assign policy_signals = "longevity-regulatory-frameworks,longevity-funding-surge" | split: "," %}
{% assign policy_keywords = "fda aging,regulatory,funding,venture capital,investment,government grant,clinical pathway,policy,nih,aging research funding" | split: "," %}

{% comment %}
  Collect all unique publishers for the source filter dropdown.
{% endcomment %}
{% assign all_publishers = "" %}
{% for post in site.posts %}
  {% if post.publisher and post.publisher != "" %}
    {% assign pub = post.publisher | strip %}
    {% unless all_publishers contains pub %}
      {% if all_publishers == "" %}
        {% assign all_publishers = pub %}
      {% else %}
        {% assign all_publishers = all_publishers | append: "|" | append: pub %}
      {% endif %}
    {% endunless %}
  {% endif %}
{% endfor %}

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Longevity & Healthspan Articles — Full Archive",
  "description": {{ page.description | jsonify }},
  "url": {{ page.url | absolute_url | jsonify }},
  "mainEntity": {
    "@type": "ItemList",
    "numberOfItems": {{ site.posts.size }},
    "itemListElement": [
      {% for post in site.posts limit: 30 %}
      {
        "@type": "ListItem",
        "position": {{ forloop.index }},
        "url": {{ post.url | absolute_url | jsonify }},
        "name": {{ post.title | jsonify }}
      }{% unless forloop.last %},{% endunless %}
      {% endfor %}
    ]
  }
}
</script>

<!-- ── Filter Panel (collapsible on mobile) ────────────── -->
<section class="filter-panel" id="filter-panel">
  <button class="filter-toggle" id="filter-toggle" aria-expanded="false" aria-controls="filter-body">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
    Filters &amp; Sort
    <span class="filter-toggle-count" id="filter-count" hidden></span>
    <svg class="filter-toggle-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
  </button>
  <div class="filter-body" id="filter-body">
    <div class="filter-row">
      <div class="filter-group">
        <label class="filter-label" for="filter-topic">Topic</label>
        <select id="filter-topic" class="filter-select">
          <option value="all">All topics</option>
          <option value="therapeutics">Treatments &amp; Drugs</option>
          <option value="biomarkers">Measuring Aging</option>
          <option value="nutrition">Food &amp; Lifestyle</option>
          <option value="technology">Science &amp; Tech</option>
          <option value="policy">Industry &amp; Access</option>
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label" for="filter-impact">Impact</label>
        <select id="filter-impact" class="filter-select">
          <option value="all">All levels</option>
          <option value="landmark">Major finding</option>
          <option value="significant">Important</option>
          <option value="noteworthy">Worth knowing</option>
          <option value="general">Background</option>
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label" for="filter-source">Source</label>
        <select id="filter-source" class="filter-select">
          <option value="all">All sources</option>
          {% assign publishers_array = all_publishers | split: "|" | sort %}
          {% for pub in publishers_array %}
          <option value="{{ pub }}">{{ pub }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label" for="filter-date-from">From</label>
        <input type="date" id="filter-date-from" class="filter-input" />
      </div>
      <div class="filter-group">
        <label class="filter-label" for="filter-date-to">To</label>
        <input type="date" id="filter-date-to" class="filter-input" />
      </div>
      <div class="filter-group">
        <label class="filter-label" for="filter-sort">Sort</label>
        <select id="filter-sort" class="filter-select">
          <option value="newest">Newest first</option>
          <option value="oldest">Oldest first</option>
          <option value="impact-desc">Highest impact</option>
          <option value="impact-asc">Lowest impact</option>
        </select>
      </div>
    </div>
    <div class="filter-actions">
      <button class="filter-reset" id="filter-reset">Clear all</button>
      <span class="filter-result-count" id="filter-result-count"></span>
    </div>
  </div>
</section>

<!-- ── Condensed Article List ──────────────────────────── -->
<section class="articles-section">
  <div class="article-list" id="article-list">
    {% for post in site.posts %}
      {% comment %} ── Compute topics ── {% endcomment %}
      {% assign topics_list = "" %}
      {% assign signal_ids_str = post.signal_ids | join: ',' | downcase %}
      {% assign source_text = post.title | append: ' ' | append: post.excerpt | downcase %}

      {% assign match = false %}
      {% for sid in therapeutics_signals %}{% if signal_ids_str contains sid %}{% assign match = true %}{% endif %}{% endfor %}
      {% if match == false %}{% for kw in therapeutics_keywords %}{% if source_text contains kw %}{% assign match = true %}{% endif %}{% endfor %}{% endif %}
      {% if match %}{% assign topics_list = topics_list | append: "therapeutics " %}{% endif %}

      {% assign match = false %}
      {% for sid in biomarkers_signals %}{% if signal_ids_str contains sid %}{% assign match = true %}{% endif %}{% endfor %}
      {% if match == false %}{% for kw in biomarkers_keywords %}{% if source_text contains kw %}{% assign match = true %}{% endif %}{% endfor %}{% endif %}
      {% if match %}{% assign topics_list = topics_list | append: "biomarkers " %}{% endif %}

      {% assign match = false %}
      {% for sid in nutrition_signals %}{% if signal_ids_str contains sid %}{% assign match = true %}{% endif %}{% endfor %}
      {% if match == false %}{% for kw in nutrition_keywords %}{% if source_text contains kw %}{% assign match = true %}{% endif %}{% endfor %}{% endif %}
      {% if match %}{% assign topics_list = topics_list | append: "nutrition " %}{% endif %}

      {% assign match = false %}
      {% for sid in tech_signals %}{% if signal_ids_str contains sid %}{% assign match = true %}{% endif %}{% endfor %}
      {% if match == false %}{% for kw in tech_keywords %}{% if source_text contains kw %}{% assign match = true %}{% endif %}{% endfor %}{% endif %}
      {% if match %}{% assign topics_list = topics_list | append: "technology " %}{% endif %}

      {% assign match = false %}
      {% for sid in policy_signals %}{% if signal_ids_str contains sid %}{% assign match = true %}{% endif %}{% endfor %}
      {% if match == false %}{% for kw in policy_keywords %}{% if source_text contains kw %}{% assign match = true %}{% endif %}{% endfor %}{% endif %}
      {% if match %}{% assign topics_list = topics_list | append: "policy " %}{% endif %}

      {% assign topics_trimmed = topics_list | strip %}

      {% comment %} ── Compute impact level ── {% endcomment %}
      {% assign impact = "general" %}
      {% assign impact_order = 4 %}
      {% assign conf = post.signal_confidence | default: "low" %}
      {% assign stance = post.signal_stance | default: "mentions" %}
      {% assign has_signals = false %}
      {% if post.signal_ids and post.signal_ids.size > 0 %}{% assign has_signals = true %}{% endif %}

      {% if conf == "medium" and has_signals and stance == "supports" %}
        {% assign impact = "landmark" %}
        {% assign impact_order = 1 %}
      {% elsif conf == "medium" or stance == "contradicts" %}
        {% assign impact = "significant" %}
        {% assign impact_order = 2 %}
      {% elsif has_signals %}
        {% assign impact = "noteworthy" %}
        {% assign impact_order = 3 %}
      {% endif %}

      {% assign pub = post.publisher | default: "" | strip %}

      <article class="article-row"
               data-topics="{{ topics_trimmed }}"
               data-impact="{{ impact }}"
               data-impact-order="{{ impact_order }}"
               data-source="{{ pub }}"
               data-date="{{ post.date | date: '%Y-%m-%d' }}">
        <div class="article-row-main">
          <div class="article-row-meta">
            <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %d, %Y" }}</time>
            {% if pub != "" %}<span class="article-source-pill" title="Source: {{ pub }}">{{ pub }}</span>{% endif %}
          </div>
          <h3 class="article-row-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        </div>
        <div class="article-row-badges">
          <span class="impact-pill impact-{{ impact }}" title="Impact: {{ impact | capitalize }}">{{ impact | capitalize }}</span>
          {% assign topic_words = topics_trimmed | split: " " %}
          {% for tw in topic_words %}
            {% if tw != "" %}<span class="topic-badge">{{ tw | capitalize }}</span>{% endif %}
          {% endfor %}
        </div>
      </article>
    {% endfor %}
  </div>
</section>
