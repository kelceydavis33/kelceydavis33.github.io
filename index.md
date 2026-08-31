---
layout: page
title: Kelcey Davis
permalink: /
lede: >-
  I am a PhD candidate in physics at the University of Connecticut and Los Alamos
  National Laboratory. I study the first billion years of galaxy and black hole
  growth with JWST, and I design the surveys that go looking for them.
---
<div class="hero">
  <img src="{{ '/assets/img/CEERS11.jpg' | relative_url }}"
       alt="A deep JWST NIRCam image of the CEERS field, dense with faint galaxies">
</div>
<figure class="bandpasses">
  {% include bandpasses.svg %}
  <figcaption class="figure-note">
    JWST NIRCam medium bands, in colour, layered over the wide bands they
    refine. Horizontal axis is wavelength in microns. Adding medium bands to
    deep wide-band imaging is what lets photometry pick out strong emission
    lines in galaxies too faint for spectroscopy.
  </figcaption>
</figure>

<p class="placeholder">
Write your bio here. Two or three paragraphs works well: what you study and why
it is interesting, how you got here, what you are working on now, and anything
you want a search committee or a journalist to know. Replace this whole block —
it lives near the top of <code>index.md</code>.
</p>

<p class="placeholder">
A second paragraph, if you want one. Teaching, outreach, the planetarium, the
SPAM programme, where you are going next.
</p>

## Research

I work on three connected problems. Each has its own page with a description
and the relevant papers.

<div class="topic-grid">
  {% for topic in site.data.topics %}
  <a class="topic-card topic-{{ topic[0] }}" href="{{ topic[1].url | relative_url }}">
    <img src="{{ topic[1].image | relative_url }}" alt="{{ topic[1].image_alt }}">
    <h2>{{ topic[1].name }}</h2>
    <p>{{ topic[1].blurb }}</p>
  </a>
  {% endfor %}
</div>

## Contact

The fastest way to reach me is email: [{{ site.email }}](mailto:{{ site.email }}).
My full publication record is on [NASA ADS]({{ site.profiles.ads }}) and my
[ORCID record]({{ site.profiles.orcid }}) is kept up to date.
