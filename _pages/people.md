---
layout: page
title: People
permalink: /people/
description: Meet the researchers and students of BRAIN.
nav: true
nav_order: 2
---

<div class="team-directory">
  {% for group in site.data.people %}
    <section class="team-group" aria-labelledby="group-{{ forloop.index }}">
      <h2 id="group-{{ forloop.index }}">{{ group.group | escape }}</h2>
      <ul class="team-members">
        {% for member in group.members %}
          <li class="team-member-item">
            {% if member.avatar %}
              <img class="member-avatar" src="{{ member.avatar | relative_url }}" alt="{{ member.name | escape }}" width="44" height="44" loading="lazy">
            {% endif %}
            <div class="member-info">
              {% if member.scholar %}
                <a href="{{ member.scholar }}" target="_blank" rel="noopener noreferrer">{{ member.name | escape }}</a>
              {% else %}
                <span class="member-name">{{ member.name | escape }}</span>
              {% endif %}
              {% if member.role %}<small>{{ member.role | escape }}</small>{% endif %}
            </div>
          </li>
        {% endfor %}
      </ul>
    </section>
  {% endfor %}
</div>

<p class="directory-source">This list is based on the <a href="https://www.imt-atlantique.fr/en/research-innovation/teams/brain/members">IMT Atlantique team directory</a> and the <a href="https://labsticc.fr/fr/lab-sticc/annuaire?pole=&team=BRAIN">Lab-STICC directory</a>.</p>
