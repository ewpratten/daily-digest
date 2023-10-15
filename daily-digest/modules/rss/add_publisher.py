import argparse
import sys
import requests
import logging
from .publisher import Publisher
from ...database import DigestDatabase
from ...env import *

logger = logging.getLogger(__name__)


def main() -> int:
    # Handle program arguments
    ap = argparse.ArgumentParser(description="Adds a publisher to the database")
    ap.add_argument("name", help="The name of the publisher")
    ap.add_argument("url", help="The URL of the publisher's RSS feed")
    ap.add_argument("--category", help="The category of the publisher's articles")
    args = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    # Ensure that the URL is valid
    logger.debug(f"Checking URL: {args.url}")
    response = requests.get(args.url)
    if not response.ok:
        logger.error(f"Failed to get URL: {args.url}")
        return 1

    # Connect to the database
    db = DigestDatabase(DATABASE_LOCATION)

    # Add the publisher to the database
    logger.debug(f"Adding publisher: {args.name}")
    publisher = Publisher(args.name, args.url, args.category)
    db.add_publisher(publisher)

    return 0


if __name__ == "__main__":
    sys.exit(main())
