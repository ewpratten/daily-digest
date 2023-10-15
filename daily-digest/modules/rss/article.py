from dataclasses import dataclass
from typing import Optional


@dataclass
class Article:
    title: str
    author: str
    url: str
    category: str
    id: Optional[int] = None
