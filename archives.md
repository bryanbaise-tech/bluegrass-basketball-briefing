---
layout: default
title: Archives
permalink: /archives/
---
<h1 class="post-title">Archives</h1>

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
{% for year in posts_by_year %}
<p class="section-label">{{ year.name }}</p>
<ul class="archive-list">
  {% for post in year.items %}
  <li class="archive-row">
    <span class="archive-date">{{ post.date | date: "%b %-d" }}</span>
    <a class="archive-link" href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>
{% endfor %}

{% if site.posts.size == 0 %}
<p>No briefings published yet.</p>
{% endif %}
