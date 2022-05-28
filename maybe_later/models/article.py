from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional

from markdownify import markdownify as md


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
        text = md(self.article_html)
        text_with_meta = f"# {self.title}\n**Source:** {self.source}\n\n{text}"
        return text_with_meta
