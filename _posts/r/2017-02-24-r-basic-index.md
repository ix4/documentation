---
description: Plotly's R graphing library makes interactive, publication-quality graphs
  online. Examples of how to make basic charts.
display_as: basic
language: r
layout: langindex
name: More Basic Charts
order: 5
page_type: example_index
permalink: r/basic-charts/
thumbnail: thumbnail/mixed.jpg
---

<header class="--welcome">
	<div class="--welcome-body">
		<!--div.--wrap-inner-->
		<div class="--title">
			<div class="--category-img"><img src="https://plot.ly/gh-pages/documentation/static/images/r-small.png" alt=""></div>
			<div class="--body">
				<h1>Plotly R Library Basic Charts</h1>
				<p>{{page.description}}</p>
			</div>
		</div>
	</div>
</header>

		{% assign languagelist = site.posts | where:"language","r" | where:"display_as","basic" | where: "layout","base" | sort: "order" %}
        {% include posts/documentation_eg.html %}