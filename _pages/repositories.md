---
layout: page
permalink: /repositories/
title: repositories
description: Code for my research and product prototypes.
nav: false
nav_order: 4
---

Find more of my work on [GitHub](https://github.com/ajaynarayanan).

<div class="projects">
  <div class="row row-cols-1 row-cols-md-2">
    {% for repo in site.data.repositories.github_repos %}
      <div class="col">
        <div class="card h-100 hoverable">
          <div class="card-body">
            <a class="project-link" href="https://github.com/{{ repo }}">
              <h2 class="card-title">{{ repo | split: '/' | last }}</h2>
              <p class="card-text">{{ site.data.repositories.descriptions[repo] }}</p>
            </a>
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
</div>
