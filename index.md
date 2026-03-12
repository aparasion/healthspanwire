---
layout: default
title: Home
nav: true
nav_order: 1
---


{% include topic-nav.html %}

<section class="post-list">
{% assign latest_date = site.posts.first.date | date: "%Y-%m-%d" %}
{% for post in site.posts %}
  <article class="post-preview">
    <h2>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>

    {% assign post_date = post.date | date: "%Y-%m-%d" %}
    <p class="post-meta">
      {{ post.date | date: "%B %d, %Y" }}
      {% if post_date == latest_date %}<span class="new-badge">NEW!</span>{% endif %}
    </p>

    <p>{{ post.excerpt }}</p>
  </article>

{% endfor %}
</section>
