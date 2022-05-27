from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Article:
    title: str
    text: str
    source: str
    category: Optional[str]
    subcategory: Optional[str]
    tags: List[str] = field(default_factory=list)
