---
layout: page
title: Research
permalink: /research/
---

My Doctoral research is broken up into three sub-areas, which you can read a bit about at each of the following pages.

<div class="topic-grid">
  {% for topic in site.data.topics %}
  <a class="topic-card topic-{{ topic[0] }}" href="{{ topic[1].url | relative_url }}">
    <img src="{{ topic[1].image | relative_url }}" alt="{{ topic[1].image_alt }}">
    <h2>{{ topic[1].name }}</h2>
    <p>{{ topic[1].blurb }}</p>
  </a>
  {% endfor %}
</div>
