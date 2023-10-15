import textwrap
import re
from datetime import datetime
from jinja2 import Template
from pathlib import Path
from typing import List
from ..modules.weather.report import WeatherReport
from ..modules.rss.article import Article


def render_email_body(
    weather_report: WeatherReport, articles: List[Article], file_name: str
) -> str:
    # Read the digest template from disk
    template_path = Path(__file__).parent / "templates" / file_name
    with open(template_path) as f:
        template = Template(f.read())

    # Reshape the articles list into {category: {author: [articles]}}
    articles_categorized = {}
    for article in articles:
        category = " " + (article.category or "Uncategorized") + " "
        # Center the category on 72 characters of :
        category = category.center(72, ":")
        if category not in articles_categorized:
            articles_categorized[category] = {}
        if article.author not in articles_categorized[category]:
            articles_categorized[category][article.author] = []
        articles_categorized[category][article.author].append(article)

    # Render
    body = template.render(
        current_date=datetime.now(),
        weather=weather_report,
        articles=articles,
        articles_categorized=articles_categorized,
        article_count=len(articles),
    )

    # If we find more than 2 consecutive newlines, replace them with 2 newlines
    body = re.sub(r"\n\n\n+", "\n\n", body)

    return body
