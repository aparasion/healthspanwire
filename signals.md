---
layout: page
title: Research Tracker
permalink: /signals/
description: "Is it real or hype? The Research Tracker follows the most-talked-about claims in longevity science and tells you where the evidence actually stands."
share: true
nav: true
nav_order: 2
---

<section class="signal-hero">
  <p class="signal-hero__desc">Is it real, or is it hype? The Research Tracker follows the most-talked-about claims in longevity science and tells you where the evidence actually stands — updated as studies, trials, and expert analyses come in.</p>

  <div class="signal-legend">
    <p class="signal-legend__title">What the status labels mean</p>
    <div class="signal-legend__pills">
      <div class="signal-legend__item">
        <span class="status-badge status-badge--supported">Well-supported</span>
        <span class="signal-legend__desc">Multiple good-quality studies in humans back this up</span>
      </div>
      <div class="signal-legend__item">
        <span class="status-badge status-badge--emerging">Early signs</span>
        <span class="signal-legend__desc">Promising but mostly in animals or very small trials — not proven yet</span>
      </div>
      <div class="signal-legend__item">
        <span class="status-badge status-badge--mixed">Conflicting evidence</span>
        <span class="signal-legend__desc">Studies point in different directions — verdict is still out</span>
      </div>
      <div class="signal-legend__item">
        <span class="status-badge status-badge--challenged">Doesn't hold up</span>
        <span class="signal-legend__desc">The weight of evidence is against this claim</span>
      </div>
    </div>
    <p class="signal-legend__note">Click any topic to browse its linked articles.</p>
  </div>
</section>

<div class="signal-grid">
  {% for signal in site.data.signals %}
    {% assign evidence_posts = site.posts | where_exp: "post", "post.signal_ids contains signal.id" %}
    {% assign display_title = signal.consumer_title | default: signal.title %}
    {% assign display_desc = signal.consumer_description | default: signal.description %}
    {% assign status_label = signal.current_status %}
    {% if signal.current_status == 'supported' %}{% assign status_label = 'Well-supported' %}
    {% elsif signal.current_status == 'emerging' %}{% assign status_label = 'Early signs' %}
    {% elsif signal.current_status == 'mixed' %}{% assign status_label = 'Conflicting evidence' %}
    {% elsif signal.current_status == 'challenged' %}{% assign status_label = "Doesn't hold up" %}
    {% endif %}
    <div class="signal-block" id="{{ signal.id }}"
         data-signal-id="{{ signal.id }}"
         data-signal-title="{{ display_title | escape }}"
         data-signal-desc="{{ display_desc | escape }}"
         data-signal-status="{{ signal.current_status }}"
         data-signal-status-label="{{ status_label | escape }}"
         data-signal-category="{{ signal.category }}"
         data-signal-date="{{ signal.first_seen }}"
         onclick="openSignalModal('{{ signal.id }}')"
         role="button"
         tabindex="0"
         onkeydown="if(event.key==='Enter'||event.key===' ')openSignalModal('{{ signal.id }}')"
         aria-label="View topic: {{ display_title | escape }}">
      <div class="signal-block__header">
        <span class="signal-block__category">{{ signal.category }}</span>
        <span class="status-badge status-badge--{{ signal.current_status }}">{{ status_label }}</span>
      </div>
      <h3 class="signal-block__title">{{ display_title }}</h3>
      <p class="signal-block__desc">{{ display_desc }}</p>
      <div class="signal-block__footer">
        <span class="signal-block__date">Since {{ signal.first_seen }}</span>
        <span class="signal-block__btn">
          {{ evidence_posts.size }} article{% if evidence_posts.size != 1 %}s{% endif %} &rarr;
        </span>
      </div>
      <button class="watch-btn" id="watch-btn-{{ signal.id }}"
              data-signal-id="{{ signal.id }}"
              onclick="event.stopPropagation(); handleWatchToggle('{{ signal.id }}')"
              aria-label="Follow topic: {{ display_title | escape }}">
        <svg class="watch-btn__icon watch-btn__icon--off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        <svg class="watch-btn__icon watch-btn__icon--on" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        <span class="watch-btn__label">Follow</span>
      </button>
    </div>
  {% endfor %}
</div>

<!-- Signal Evidence Modal -->
<div class="signal-modal-overlay" id="signal-modal-overlay" role="dialog" aria-modal="true" aria-labelledby="signal-modal-title" hidden>
  <div class="signal-modal">
    <div class="signal-modal__header">
      <div class="signal-modal__meta">
        <span class="signal-modal__category" id="signal-modal-category"></span>
        <span id="signal-modal-status"></span>
      </div>
      <button class="signal-modal__close" onclick="closeSignalModal()" aria-label="Close">&#x2715;</button>
    </div>
    <h2 class="signal-modal__title" id="signal-modal-title"></h2>
    <p class="signal-modal__desc" id="signal-modal-desc"></p>
    <div class="signal-modal__posts-label">Articles covering this</div>
    <div class="signal-modal__posts" id="signal-modal-posts"></div>
    <div class="signal-modal__actions">
      <button class="watch-btn watch-btn--modal" id="watch-btn-modal"
              onclick="handleWatchToggle(currentModalSignalId)"
              aria-label="Follow this topic">
        <svg class="watch-btn__icon watch-btn__icon--off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        <svg class="watch-btn__icon watch-btn__icon--on" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        <span class="watch-btn__label">Follow this topic</span>
      </button>
      <div class="signal-modal__share" id="signal-modal-share"></div>
    </div>
  </div>
</div>

<script>
var currentModalSignalId = null;

const SIGNAL_POSTS = {
  {% for signal in site.data.signals %}
    {% assign evidence_posts = site.posts | where_exp: "post", "post.signal_ids contains signal.id" %}
    {{ signal.id | jsonify }}: [
      {% for post in evidence_posts %}
        {
          "title": {{ post.title | jsonify }},
          "url": {{ post.url | relative_url | jsonify }},
          "date": {{ post.date | date: "%b %d, %Y" | jsonify }},
          "stance": {{ post.signal_stance | default: "" | jsonify }}
        }{% unless forloop.last %},{% endunless %}
      {% endfor %}
    ]{% unless forloop.last %},{% endunless %}
  {% endfor %}
};

// ── Follow Button Logic ────────────────────────────────────
function refreshAllWatchButtons() {
  document.querySelectorAll('.watch-btn[data-signal-id]').forEach(function (btn) {
    var id = btn.getAttribute('data-signal-id');
    var isWatched = window.isSignalWatched && window.isSignalWatched(id);
    btn.classList.toggle('is-watched', isWatched);
    var label = btn.querySelector('.watch-btn__label');
    if (label) label.textContent = isWatched ? 'Following' : 'Follow';
    btn.setAttribute('aria-label', isWatched ? 'Stop following topic' : 'Follow topic');
  });
}

function refreshModalWatchButton() {
  var modalBtn = document.getElementById('watch-btn-modal');
  if (!modalBtn || !currentModalSignalId) return;
  var isWatched = window.isSignalWatched && window.isSignalWatched(currentModalSignalId);
  modalBtn.classList.toggle('is-watched', isWatched);
  var label = modalBtn.querySelector('.watch-btn__label');
  if (label) label.textContent = isWatched ? 'Following this topic' : 'Follow this topic';
  modalBtn.setAttribute('aria-label', isWatched ? 'Stop following this topic' : 'Follow this topic');
}

function handleWatchToggle(signalId) {
  if (!signalId || !window.toggleWatchSignal) return;
  window.toggleWatchSignal(signalId);
  refreshAllWatchButtons();
  refreshModalWatchButton();
}

// Initialize: randomize signal order + follow button states on load
document.addEventListener('DOMContentLoaded', function () {
  var grid = document.querySelector('.signal-grid');
  var blocks = Array.prototype.slice.call(grid.children);
  for (var i = blocks.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    grid.appendChild(blocks[j]);
    blocks[j] = blocks[i];
  }
  refreshAllWatchButtons();
});

function openSignalModal(signalId) {
  currentModalSignalId = signalId;
  var block = document.getElementById(signalId);
  var overlay = document.getElementById('signal-modal-overlay');

  document.getElementById('signal-modal-title').textContent = block.dataset.signalTitle;
  document.getElementById('signal-modal-desc').textContent = block.dataset.signalDesc;

  var catEl = document.getElementById('signal-modal-category');
  catEl.textContent = block.dataset.signalCategory;

  var statusEl = document.getElementById('signal-modal-status');
  statusEl.textContent = block.dataset.signalStatusLabel || block.dataset.signalStatus;
  statusEl.className = 'status-badge status-badge--' + block.dataset.signalStatus;

  var postsEl = document.getElementById('signal-modal-posts');
  var posts = SIGNAL_POSTS[signalId] || [];

  var stanceLabels = { supports: 'Supports', contradicts: 'Contradicts', mixed: 'Mixed', mentions: 'Mentions' };

  if (posts.length === 0) {
    postsEl.innerHTML = '<p class="signal-modal__empty">No linked articles yet.</p>';
  } else {
    postsEl.innerHTML = '<ul class="signal-modal__list">' +
      posts.map(function(p) {
        var stancePill = p.stance ? '<span class="stance-badge stance-badge--' + p.stance + '">' + (stanceLabels[p.stance] || p.stance) + '</span>' : '';
        return '<li class="signal-modal__item">' +
          '<a href="' + p.url + '" class="signal-modal__link">' + p.title + '</a>' +
          '<div class="signal-modal__item-meta"><span class="signal-modal__date">' + p.date + '</span>' + stancePill + '</div>' +
          '</li>';
      }).join('') +
    '</ul>';
  }

  var shareEl = document.getElementById('signal-modal-share');
  var sigUrl = window.location.origin + window.location.pathname.replace(/\/$/, '') + '/#' + signalId;
  shareEl.innerHTML = '<a class="signal-modal__share-link" href="' + sigUrl + '" target="_blank" rel="noopener">&#128279; Permalink to this topic</a>';

  overlay.hidden = false;
  document.body.classList.add('modal-open');
  refreshModalWatchButton();
}

function closeSignalModal() {
  currentModalSignalId = null;
  document.getElementById('signal-modal-overlay').hidden = true;
  document.body.classList.remove('modal-open');
}

document.getElementById('signal-modal-overlay').addEventListener('click', function(e) {
  if (e.target === this) closeSignalModal();
});

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeSignalModal();
});
</script>
