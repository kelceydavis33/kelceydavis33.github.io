---
layout: page
title: Kelcey Davis
permalink: /
lede: >-
  I am a PhD candidate in physics at the University of Connecticut and Los Alamos
  National Laboratory. I study the time period when the earliest supermassive black holes and the galaxies that host them first grew, Cosmic Dawn.
---
<div class="hero">
  <img src="{{ '/assets/img/CEERS11.jpg' | relative_url }}"
       alt="Cropped Image from the CEERS Early Release Science Program, the field of view from JWST where I conduct most of my research. ">
</div>


I am an observational astrophysicist interested in the environments of the earliest supermassive black holes and the galaxies that host them. In my doctoral thesis, I am demonstrating how strong line emission can be recovered from the broadband photometry alone in many of these early systems. My photometric galaxy catalog has provided target selections for several spectroscopic surveys (OCEANS, THRILS, and CEERS). The work has also partly inspired the award of 60 hours of additional photometric observations in the CEERS legacy footprint through SPAM, a recently executed program which I PI'ed. My science publications on strong emission line sources at cosmic dawn concern quantifying the presence of accreting supermassive black holes, studying the nature of emission line excitation mechanisms in extreme systems, and tracing gas kinematics in JWST's ``Little Red Dots''. In addition to research activities I maintain active commitments to science outreach and undergraduate research mentorship.



## Research

My research with JWST spans Extreme Emission Line Galaxies, Little Red Dots, and Observational Planning. Each of these topics is detailed below with my relevant papers listed. I have done research across many other topics. During my PhD work, I spent a summer interning in computational physics calculating plasma opacities, which is reflected in my publication record. Other research topics have included 21cm radio cosmology, the subject of my undergraduate thesis, but also CMB instrumentation, bench top optical physics, and variable stars. I am drawn to interesting problems which frequently brings me to other areas of research. 

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
