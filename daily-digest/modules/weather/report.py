from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class WeatherReport:
    current_temperature_c: float
    current_summary: str
    updated_at: datetime
    urls: Dict[str, str]
