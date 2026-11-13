---
layout: page
title: Announcements
permalink: /announcements/
description: News and updates from the BRAIN team.
nav: true
nav_order: 3
---

{% if site.news != empty %}
  {% include news.liquid %}
{% else %}
  <p>Team announcements will appear here.</p>
{% endif %}
