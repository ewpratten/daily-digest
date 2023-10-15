import requests
import logging
import feedparser
import re
import pytz
import textwrap
from datetime import datetime
from ..report import WeatherReport

logger = logging.getLogger(__name__)

CURRENT_TEMPERATURE_RE = re.compile(r"Current Conditions:\s+([\d\.]+).C")


def get_weather_report(province: str, location_id: int, digest_mode: str) -> WeatherReport:
    # Make a request for the location's forecast RSS feed
    url = f"https://weather.gc.ca/rss/city/{province}-{location_id}_e.xml"
    logger.debug(f"Requesting weather report from: {url}")
    response = requests.get(url)

    # If the request failed, raise an exception
    if response.status_code != 200:
        raise Exception(
            f"Failed to get weather report. Status code: {response.status_code}. Response: {response.text}"
        )

    # Parse the RSS response
    feed = feedparser.parse(response.text)
    
    # Find the entry with category "Current Conditions"
    current_conditions = None
    for entry in feed.entries:
        if entry.category == "Current Conditions":
            current_conditions = entry
            break
    else:
        raise Exception("Failed to find entry with category 'Current Conditions'")
    
    # Find the first "Weather Forecasts" entry 
    weather_forecast = None
    for entry in feed.entries:
        if entry.category == "Weather Forecasts":
            weather_forecast = entry
            break
    else:
        raise Exception("Failed to find entry with category 'Weather Forecasts'")
    
    # Parse the current temperature
    current_temperature = float(CURRENT_TEMPERATURE_RE.search(current_conditions.title).group(1))
    
    # The updated timestamp is in UTC, so we need to convert it to the local timezone
    updated_utc = datetime.fromisoformat(weather_forecast["updated"])
    updated = updated_utc.astimezone(pytz.timezone("America/Toronto"))
    
    # Select the appropriate summary prefix
    summary_prefix = {
        "morning": "Daytime weather is expected to be",
        "evening": "Tonight's weather is expected to be",
    }[digest_mode]
    
    # Lowercase the first word of the summary
    first_word = weather_forecast.summary.split()[0]
    summary = summary_prefix + " " + first_word.lower() + " "
    summary += " ".join(weather_forecast.summary.split()[1:])
    
    # Split off the final "Forecast issued" part of the summary
    summary = summary.split(". Forecast issued")[0] + "."
    
    # Wrap the summary to be email-friendly
    summary = "\n".join(textwrap.wrap(summary, width=72))
    
    # Construct a WeatherReport object
    return WeatherReport(
        current_temperature_c=current_temperature,
        current_summary=summary,
        updated_at=updated,
        urls={
            "Daily": f"https://weather.gc.ca/city/pages/{province}-{location_id}_metric_e.html",
            "Hourly": f"https://weather.gc.ca/forecast/hourly/{province}-{location_id}_metric_e.html",
        }
    )
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Getting test weather report for Oakville, ON")
    print(get_weather_report("on", 79, "morning"))