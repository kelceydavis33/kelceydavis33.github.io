---
layout: page
title: Research
permalink: /research/
---

I am an observational astrophysicist interested in the environments of the earliest supermassive black holes and the galaxies that host them. In my doctoral thesis, I have demonstrated how strong line emission can be recovered from the broadband photometry in many of these early systems. This photometric galaxy catalog has provided target selections for several spectroscopic surveys (OCEANS, THRILS, and CEERS). The work has also inspired the award of 60 hours of additional photometric observations in the CEERS legacy footprint through SPAM, a recently executed program which I PI'ed. My science publications on strong emission line sources at cosmic %noon to 
% dawn concern quantifying the presence of accreting supermassive black holes, studying the nature of the emission line excitation mechanisms, and tracing gas kinematics in JWST's ``Little Red Dots''. In addition to research activities I maintain active commitments to science outreach and undergraduate research mentorship.

<div class="topic-grid">
  {% for topic in site.data.topics %}
  <a class="topic-card topic-{{ topic[0] }}" href="{{ topic[1].url | relative_url }}">
    <img src="{{ topic[1].image | relative_url }}" alt="{{ topic[1].image_alt }}">
    <h2>{{ topic[1].name }}</h2>
    <p>{{ topic[1].blurb }}</p>
  </a>
  {% endfor %}
</div>
