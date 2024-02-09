import argparse
import sys
import logging
from datetime import datetime
from requests.exceptions import ConnectTimeout, ConnectionError

from .modules.weather.sources.environment_canada import get_weather_report
from .modules.rss.fetch import get_articles_by_publisher
from .email import render_email_body, send_email
from .database import DigestDatabase
from .env import *

logger = logging.getLogger(__name__)


def main() -> int:
    # Handle program arguments
    ap = argparse.ArgumentParser(prog="daily-digest")
    ap.add_argument(
        "--digest-type",
        help="The type of digest to send",
        choices=["morning", "evening"],
        default="morning",
    )
    ap.add_argument("--dry-run", help="Do not send emails", action="store_true")
    ap.add_argument(
        "--verbose", "-v", help="Enable verbose logging", action="store_true"
    )
    ap.add_argument(
        "--no-mark-sent",
        help="Don't mark sent articles as sent (for debugging)",
        action="store_true",
    )
    ap.add_argument(
        "--no-fetch-articles", help="Don't fetch articles", action="store_true"
    )
    args = ap.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # Connect to the database
    db = DigestDatabase(DATABASE_LOCATION)

    # Fetch articles into the database
    if not args.no_fetch_articles:
        logger.info("Fetching list of publishers")
        publishers = db.get_publishers()
        logger.info(f"Found {len(publishers)} publishers")
        for publisher in publishers:
            try:
                articles = get_articles_by_publisher(publisher)
            except ConnectTimeout as e:
                logger.warning(f"Timed out trying to fetch articles from {publisher.name}: {e}")
                continue
            except ConnectionError as e:
                logger.warning(f"Failed to fetch articles from {publisher.name}: {e}")
                continue

            # Add to the database
            logger.info(
                f"Found {len(articles)} articles from {publisher.name}. Adding to database"
            )
            for article in articles:
                db.add_article(article, publisher)

    # Read needed data
    #weather = get_weather_report(
    #    WEATHER_REGION, int(WEATHER_LOCATION_ID), args.digest_type
    #)
    articles = db.get_unsent_articles()

    # Render the email body
    body = render_email_body(
        #weather,
        None,
        articles,
        {"morning": "morning_digest.txt", "evening": "evening_digest.txt"}[
            args.digest_type
        ],
    )

    # If we are in dry-run mode, print the email body and exit
    if args.dry_run:
        print("Dry-run mode enabled. Email body:\n---")
        print(body)
        print("---")
    else:
        # Handle email sending
        send_email(
            EMAIL_DESTINATION,
            f"Your digest for {datetime.now().strftime('%A, %B %d')}",
            body,
        )

    # Mark all articles as sent
    if not args.no_mark_sent:
        if args.digest_type == "morning":
            logger.info("Marking all articles as sent")
            for article in articles:
                db.mark_article_sent(article.id)
        else:
            logger.info(
                "Not marking articles as sent because this is an evening digest"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
