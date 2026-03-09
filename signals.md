---
layout: page
title: Signal Tracker
permalink: /signals/
nav: true
nav_order: 3
---

A living tracker of high-impact claims in localization and AI, with linked evidence from published coverage.

<div class="signal-directory">
  <h2 class="signal-directory__heading">Browse Signals</h2>
  <div class="signal-directory__grid">
    {% for signal in site.data.signals %}
      {% assign evidence_posts = site.posts | where_exp: "post", "post.signal_ids contains signal.id" %}
      <a href="#signal-{{ signal.id }}" class="signal-tile">
        <span class="signal-tile__category">{{ signal.category }}</span>
        <span class="signal-tile__title">{{ signal.title }}</span>
        <span class="signal-tile__footer">
          <span class="status-badge status-badge--{{ signal.current_status }}">{{ signal.current_status }}</span>
          <span class="signal-tile__count">{{ evidence_posts.size }} post{% if evidence_posts.size != 1 %}s{% endif %}</span>
        </span>
      </a>
    {% endfor %}
  </div>
</div>

---

{% for signal in site.data.signals %}
  {% assign evidence_posts = site.posts | where_exp: "post", "post.signal_ids contains signal.id" %}
  <article class="signal-card" id="signal-{{ signal.id }}">
    <h2>{{ signal.title }}</h2>
    <p class="post-meta">Category: {{ signal.category }} · Status: <span class="status-badge status-badge--{{ signal.current_status }}">{{ signal.current_status }}</span> · First seen: {{ signal.first_seen }}</p>
    <p>{{ signal.description }}</p>

    {% if evidence_posts.size > 0 %}
      <ul class="signal-evidence-list">
        {% for post in evidence_posts limit: 8 %}
          <li>
            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
            <span class="signal-evidence-meta">({{ post.date | date: "%Y-%m-%d" }}{% if post.signal_stance %}, <span class="stance-badge stance-badge--{{ post.signal_stance }}">{{ post.signal_stance }}</span>{% endif %})</span>
          </li>
        {% endfor %}
      </ul>
    {% else %}
      <p class="signal-card__empty">No linked evidence yet.</p>
    {% endif %}
  </article>
{% endfor %}
