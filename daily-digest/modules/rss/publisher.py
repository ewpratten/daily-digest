from dataclasses import dataclass
from typing import Optional


@dataclass
class Publisher:
    name: str
    rss_url: str
    category: Optional[str] = None
    id: Optional[int] = None
