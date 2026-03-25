---
layout: page
title: Monthly Reports
permalink: /monthly-reports/
nav: true
nav_order: 3
---

A monthly intelligence report synthesizing the most significant developments in longevity science, healthspan research, and aging biology — covering therapeutics, biomarkers, nutrition, technology, and policy.
<br />
{% assign monthly_posts = site.posts | where_exp: "post", "post.categories contains 'monthly-summary'" %}
{% if monthly_posts.size > 0 %}
  <section class="post-list">
  {% for post in monthly_posts %}
    {% assign source_text = post.title | append: ' ' | append: post.excerpt | append: ' ' | append: post.content | downcase %}
    {% assign topics = '' %}
    {% if source_text contains 'therapeutics' or source_text contains 'senolytic' or source_text contains 'therapy' or source_text contains 'clinical' or source_text contains 'treatment' or source_text contains 'drug' %}
      {% assign topics = topics | append: 'therapeutics,' %}
    {% endif %}
    {% if source_text contains 'biomarker' or source_text contains 'epigenetic' or source_text contains 'clock' or source_text contains 'aging biology' or source_text contains 'longevity' %}
      {% assign topics = topics | append: 'biomarkers,' %}
    {% endif %}
    {% if source_text contains 'nutrition' or source_text contains 'diet' or source_text contains 'fasting' or source_text contains 'caloric' or source_text contains 'supplement' %}
      {% assign topics = topics | append: 'nutrition,' %}
    {% endif %}
    {% if source_text contains 'ai' or source_text contains 'machine learning' or source_text contains 'platform' or source_text contains 'technology' or source_text contains 'tool' or source_text contains 'software' %}
      {% assign topics = topics | append: 'technology,' %}
    {% endif %}
    {% if source_text contains 'regulation' or source_text contains 'law' or source_text contains 'fda' or source_text contains 'government' or source_text contains 'policy' or source_text contains 'approval' %}
      {% assign topics = topics | append: 'policy,' %}
    {% endif %}
    {% if topics == '' %}
      {% assign topics = 'biomarkers' %}
    {% endif %}

    <article class="post-preview" data-topics="{{ topics | strip }}">
      <h2>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </h2>

      <p class="post-meta">
        {{ post.date | date: "%B %d, %Y" }}
      </p>

      <p>{{ post.excerpt }}</p>
    </article>
  {% endfor %}
  </section>
{% else %}
  <p>No monthly reports have been published yet.</p>
{% endif %}
