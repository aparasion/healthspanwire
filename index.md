---
layout: default
title: Home
nav: true
nav_order: 1
---

<section class="hero">
  <div class="hero-content">
    <h1>The pulse of the language services industry</h1>
    <p class="hero-subtitle">Daily coverage of translation, localization, and AI — curated, analyzed, and tracked through the signals that matter.</p>
    <div class="hero-stats">
      <div class="hero-stat">
        <span class="hero-stat-number">{{ site.posts.size }}</span>
        <span class="hero-stat-label">Articles</span>
      </div>
      <div class="hero-stat">
        <span class="hero-stat-number">{{ site.data.signals.size }}</span>
        <span class="hero-stat-label">Signals</span>
      </div>
      <div class="hero-stat">
        <span class="hero-stat-number">5</span>
        <span class="hero-stat-label">Topics</span>
      </div>
    </div>
  </div>
</section>

{% include topic-nav.html %}

{% assign latest_date = site.posts.first.date | date: "%Y-%m-%d" %}

<section class="articles-section">

  <article class="featured-article reveal">
    <span class="featured-badge">Latest</span>
    <h2><a href="{{ site.posts.first.url | relative_url }}">{{ site.posts.first.title }}</a></h2>
    <p class="post-meta">{{ site.posts.first.date | date: "%B %d, %Y" }}</p>
    <p>{{ site.posts.first.excerpt | strip_html | truncate: 200 }}</p>
  </article>

  <div class="post-grid reveal-stagger">
    {% for post in site.posts offset:1 %}
      <article class="post-card">
        <p class="post-meta">{{ post.date | date: "%B %d, %Y" }}{% assign post_date = post.date | date: "%Y-%m-%d" %}{% if post_date == latest_date %}<span class="new-badge">NEW</span>{% endif %}</p>
        <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
        <p>{{ post.excerpt | strip_html | truncate: 140 }}</p>
        <span class="read-more">Read more &rarr;</span>
      </article>
    {% endfor %}
  </div>

</section>
