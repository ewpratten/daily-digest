import os
from pathlib import Path

WEATHER_REGION = os.environ.get("DD_WEATHER_REGION", "on")
WEATHER_LOCATION_ID = os.environ.get("DD_WEATHER_LOCATION_ID", 79)
DATABASE_LOCATION = os.environ.get(
    "DD_DATABASE_LOCATION", Path(__file__).parent.parent / "daily_digest.sqlite3"
)
SMTP_SERVER = os.environ.get("DD_SMTP_SERVER", "smtp.ewpratten.com")
SMTP_PORT = os.environ.get("DD_SMTP_PORT", 587)
SMTP_USERNAME = os.environ.get("DD_SMTP_USERNAME", "digest-bot@ewpratten.com")
SMTP_PASSWORD = os.environ["DD_SMTP_PASSWORD"]
EMAIL_DESTINATION = os.environ.get("DD_EMAIL_DESTINATION", "evan@ewpratten.com")