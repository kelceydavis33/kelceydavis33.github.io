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

<section class="papers">
  <h2>All publications</h2>

  {% if site.data.publications.papers.size == 0 %}
  <p class="empty">
    No publications loaded yet. Add your <code>ADS_TOKEN</code> repository secret
    and run the <em>Build site and refresh publications</em> workflow from the
    Actions tab.
  </p>
  {% else %}
    {% assign by_year = site.data.publications.papers | group_by: "year" %}
    {% for group in by_year %}
    <h3 class="year-heading">{{ group.name }}</h3>
    {% include paper-list.html papers=group.items %}
    {% endfor %}
  {% endif %}
</section>
