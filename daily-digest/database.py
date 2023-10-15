import sqlite3
import logging
from pathlib import Path
from typing import List, Optional
from .modules.rss.article import Article
from .modules.rss.publisher import Publisher

logger = logging.getLogger(__name__)


class DigestDatabase:
    connection: sqlite3.Connection

    def __init__(self, db_path: str):
        logger.info(f"Connecting to database: {db_path}")
        self.connection = sqlite3.connect(db_path)

        # Create the tables if they don't exist
        logger.debug("Running schema.sql")
        with open(Path(__file__).parent / "schema.sql") as f:
            self.connection.executescript(f.read())
        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def get_unsent_articles(self) -> List[Article]:
        # Find all articles that have not been sent
        logger.debug("Getting unsent articles")
        cursor = self.connection.execute(
            "SELECT id, title, author, url, category, publisher_id FROM articles WHERE sent = 0"
        )

        # Convert the results into Article objects
        articles = []
        for row in cursor:
            
            # Find the publisher for this article
            publisher = None
            publisher_cursor = self.connection.execute(
                "SELECT id, name, rss_url, category FROM publishers WHERE id = ?",
                (row[5],)
            )
            publisher_row = publisher_cursor.fetchone()
            if publisher_row is not None:
                publisher = Publisher(
                    id=publisher_row[0],
                    name=publisher_row[1],
                    rss_url=publisher_row[2],
                    category=publisher_row[3],
                )
            
            articles.append(
                Article(
                    id=row[0],
                    title=row[1],
                    author=publisher.name,
                    url=row[3],
                    category=publisher.category,
                )
            )

        return articles

    def add_article(self, article: Article, publisher: Publisher):
        # Check if the article already exists
        logger.debug(f"Checking if article exists: {article.title}")
        cursor = self.connection.execute(
            "SELECT id FROM articles WHERE title = ? AND url = ?",
            (article.title, article.url),
        )
        row = cursor.fetchone()
        if row is not None:
            logger.debug(f"Article already exists: {article.title}")
            return

        # Insert the article into the database
        logger.debug(f"Adding article: {article.title}")
        self.connection.execute(
            "INSERT INTO articles (title, author, url, category, publisher_id) VALUES (?, ?, ?, ?, ?)",
            (
                article.title,
                article.author,
                article.url,
                article.category,
                publisher.id,
            ),
        )
        self.connection.commit()

    def mark_article_sent(self, article_id: int):
        # Set the `sent` column to 1 for the given article ID
        logger.debug(f"Marking article as sent: {article_id}")
        self.connection.execute(
            "UPDATE articles SET sent = 1 WHERE id = ?",
            (article_id,),
        )
        self.connection.commit()

    def add_publisher(self, publisher: Publisher):
        # If the publisher already exists, return
        logger.debug(f"Checking if publisher exists: {publisher.name}")
        cursor = self.connection.execute(
            "SELECT id FROM publishers WHERE rss_url = ?", (publisher.rss_url,)
        )
        row = cursor.fetchone()
        if row is not None:
            logger.debug(f"Publisher already exists: {publisher.name}")
            return
        
        # Insert the publisher into the database
        logger.debug(f"Adding publisher: {publisher.name}")
        self.connection.execute(
            "INSERT INTO publishers (name, rss_url, category) VALUES (?, ?, ?)",
            (publisher.name, publisher.rss_url, publisher.category),
        )
        self.connection.commit()

    def get_publishers(self) -> List[Publisher]:
        # Find all publishers
        logger.debug("Getting publishers")
        cursor = self.connection.execute(
            "SELECT id, name, rss_url, category FROM publishers"
        )

        # Convert the results into Publisher objects
        publishers = []
        for row in cursor:
            publishers.append(
                Publisher(
                    id=row[0],
                    name=row[1],
                    rss_url=row[2],
                    category=row[3],
                )
            )

        return publishers
