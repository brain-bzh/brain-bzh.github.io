---
layout: brain
permalink: /publications/
title: Publications
description: Publications of the BRAIN team, refreshed weekly from HAL.
stylesheet: /assets/publications.css
module: /assets/js/bibsearch.js
nav: true
nav_order: 1
---
<div class="pub-tools">
  <div class="filter-row">
    <span class="filter-label">Topics</span>
    <div class="filter-pills">
      <button type="button" class="filter-pill is-active" data-term="">All</button>
      {% for theme in site.data.themes.themes %}
      <button type="button" class="filter-pill" data-term="{{ theme.label | escape }}">{{ theme.label }}</button>
      {% endfor %}
    </div>
  </div>
  <div class="filter-row">
    <label class="filter-label" for="author-filter">Author</label>
    <select id="author-filter" class="pub-select">
      <option value="">Anyone</option>
      {% for group in site.data.people %}
      <optgroup label="{{ group.group | escape }}">
        {% for member in group.members %}
        <option value="{{ member.name | escape }}">{{ member.name }}</option>
        {% endfor %}
      </optgroup>
      {% endfor %}
    </select>
    <label class="sr-only" for="bibsearch">Search publications</label>
    <input type="search" id="bibsearch" class="pub-search" spellcheck="false" autocomplete="off" placeholder="Search titles, authors, venues, years">
  </div>
</div>

<div class="publication-stats-bar" id="publication-stats-bar" aria-live="polite">
  <div class="pub-count-status">
    <span id="pub-count-text">Loading publications…</span>
    <button type="button" class="pub-reset-btn is-hidden" id="pub-reset-btn">Reset filter ×</button>
  </div>
  <div class="pub-year-chart" id="pub-year-chart" aria-label="Filter publications by year"></div>
</div>

<div class="publications">
{% bibliography %}
</div>

<p class="pub-note">Topics are assigned automatically from HAL titles, keywords and abstracts. Records whose affiliation is not recorded in HAL may be missing.</p>
