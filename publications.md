---
layout: page
title: Publications
permalink: /publications/
---

{% assign stats = site.data.publications.stats %}
{% assign cloud = site.data.wordcloud %}

{% if cloud.words and cloud.words.size > 0 %}
<div class="wordcloud">
  {% for word in cloud.words %}<a class="w{{ word.weight }}" href="{{ word.url }}">{{ word.text }}</a> {% endfor %}
</div>
<p class="figure-note">
Terms that appear most often across these papers, sized by how often they turn
up. Built from the NASA ADS word cloud service; each term links to a search for
that word inside my publication record.
</p>
{% endif %}

<dl class="stats">
  <div><dt>Publications</dt><dd>{{ stats.n_papers }}</dd></div>
  <div><dt>Refereed</dt><dd>{{ stats.n_refereed }}</dd></div>
  <div><dt>First author</dt><dd>{{ stats.n_first_author }}</dd></div>
  <div><dt>Citations</dt><dd>{{ stats.citations_total }}</dd></div>
  <div><dt>h-index</dt><dd>{{ stats.h_index }}</dd></div>
  <div><dt>i10-index</dt><dd>{{ stats.i10_index }}</dd></div>
</dl>

<p class="updated">
  Last refreshed {{ stats.updated }} from
  <a href="{{ site.profiles.ads }}">NASA ADS</a>, and updated automatically on
  the first of each month. Citation counts include refereed and unrefereed work.
</p>

{% comment %}
  Papers are split by your place in the author list, newest first within
  each section. Shared first-author papers marked co_first in
  _data/paper_topics.yml count as first author, as on the research pages.
  To rename a section, edit its heading in the list just below.
{% endcomment %}

{% if site.data.publications.papers.size == 0 %}
<section class="papers">
  <h2>Publications</h2>
  <p class="empty">
    No publications loaded yet. Add your <code>ADS_TOKEN</code> repository secret
    and run the <em>Build site and refresh publications</em> workflow from the
    Actions tab.
  </p>
</section>
{% else %}
{% assign sections = "first|First author,second|Second author,other|Contributing author" | split: "," %}
{% for section in sections %}
{% assign section_key = section | split: "|" | first %}
{% assign section_heading = section | split: "|" | last %}
{% assign section_count = 0 %}
{% assign last_year = "" %}
{% capture section_list %}
  {% for paper in site.data.publications.papers %}
    {% assign entry = site.data.paper_topics[paper.bibcode] %}
    {% if paper.author_position == 1 or entry.co_first %}
      {% assign paper_section = "first" %}
    {% elsif paper.author_position == 2 %}
      {% assign paper_section = "second" %}
    {% else %}
      {% assign paper_section = "other" %}
    {% endif %}
    {% if paper_section == section_key %}
      {% if paper.year != last_year %}
        {% if section_count > 0 %}</ul>{% endif %}
        <h3 class="year-heading">{{ paper.year }}</h3>
        <ul class="paper-list">
        {% assign last_year = paper.year %}
      {% endif %}
      {% include paper-entry.html paper=paper %}
      {% assign section_count = section_count | plus: 1 %}
    {% endif %}
  {% endfor %}
  {% if section_count > 0 %}</ul>{% endif %}
{% endcapture %}
<section class="papers">
  <h2>{{ section_heading }} ({{ section_count }})</h2>
  {% if section_count > 0 %}
  {{ section_list }}
  {% else %}
  <p class="empty">None yet.</p>
  {% endif %}
</section>
{% endfor %}
{% endif %}
