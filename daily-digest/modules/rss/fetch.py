import requests
import logging
import feedparser
from typing import List
from .publisher import Publisher
from .article import Article

logger = logging.getLogger(__name__)


def get_articles_by_publisher(publisher: Publisher) -> List[Article]:
    # Query the RSS feed
    logger.debug(f"Getting articles from {publisher.name}")
    response = requests.get(publisher.rss_url)

    # If the request failed, raise an exception
    if response.status_code != 200:
        logger.error(
            f"Failed to get articles from {publisher.name}. Status code: {response.status_code}. Response: {response.text}"
        )
        return []

    # Parse the RSS response
    feed = feedparser.parse(response.text)

    # Convert the feed entries into Article objects
    articles = []
    for entry in feed.entries:
        # If we have a paid LWN article, skip it
        if publisher.rss_url == "http://lwn.net/headlines/Features" and entry.title.startswith("[$]"):
            logger.info(f"Skipping paid LWN article: {entry.title}")
            continue
        
        articles.append(
            Article(
                title=entry.title,
                author=publisher.name,
                url=entry.get("link", entry.get("guid", "")),
                category=publisher.category,
            )
        )

    return articles
