import argparse
import sys
import logging
import opml
import requests
from .publisher import Publisher
from ...database import DigestDatabase
from ...env import *

logger = logging.getLogger(__name__)


def main() -> int:
    # Handle program arguments
    ap = argparse.ArgumentParser(description="Adds the contents of an OPML file to the database")
    ap.add_argument("file", help="The file to read")
    ap.add_argument("--no-verify", help="Don't verify the URLs", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    
    # Read the OPML file
    logger.debug(f"Reading OPML file: {args.file}")
    with open(args.file) as f:
        opml_data = opml.parse(f)
        
    # The outer outlines are categories
    if not args.no_verify:
        for category in opml_data:
            # The inner outlines are publishers
            for publisher in category:
                # Ensure that the URL is valid
                logger.debug(f"Checking URL: {publisher.xmlUrl}")
                response = requests.get(publisher.xmlUrl)
                if not response.ok:
                    logger.error(f"Failed to get URL: {publisher.xmlUrl}")
                    return 1

    # Connect to the database
    db = DigestDatabase(DATABASE_LOCATION)
    
    # Add the publishers to the database
    for category in opml_data:
        for publisher in category:
            logger.debug(f"Adding publisher: {publisher.text} ({publisher.xmlUrl}) to {category.text}")
            db.add_publisher(Publisher(publisher.text, publisher.xmlUrl, category.text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
