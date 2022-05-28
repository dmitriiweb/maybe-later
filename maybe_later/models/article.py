from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional


class ArticleStatus(Enum):
    NEW = auto()


@dataclass
class Article:
    title: str
    text: str
    article_html: str
    source: str
    category: Optional[str]
    subcategory: Optional[str]
    tags: List[str] = field(default_factory=list)
    status: ArticleStatus = ArticleStatus.NEW

    def to_markdown(self) -> str:
        pass
