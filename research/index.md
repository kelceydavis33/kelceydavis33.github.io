---
layout: page
title: Research
permalink: /research/
---

<p class="placeholder">
Write your research summary here. This is the paragraph that ties the three
threads below together — the question you are really asking, and why these
three lines of work are the way you are answering it. A reader who stops after
this paragraph should still know what you do. Replace this block in
<code>research/index.md</code>.
</p>

<div class="topic-grid">
  {% for topic in site.data.topics %}
  <a class="topic-card topic-{{ topic[0] }}" href="{{ topic[1].url | relative_url }}">
    <img src="{{ topic[1].image | relative_url }}" alt="{{ topic[1].image_alt }}">
    <h2>{{ topic[1].name }}</h2>
    <p>{{ topic[1].blurb }}</p>
  </a>
  {% endfor %}
</div>
