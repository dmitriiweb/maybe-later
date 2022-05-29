from dataclasses import dataclass, field
from typing import List, Optional

from markdownify import markdownify as md

from maybe_later._types import ArticleStatus


@dataclass
class MetaModel:
    title: str
    source: str
    category: Optional[str]
    subcategory: Optional[str]
    tags: List[str] = field(default_factory=list)
    status: ArticleStatus = ArticleStatus.UNREAD


@dataclass
class ArticleModel:
    meta: MetaModel
    text: str
    article_html: str

    def to_markdown(self) -> str:
        text = md(self.article_html)
        text_with_meta = (
            f"# {self.meta.title}\n**Source:** {self.meta.source}\n\n{text}"
        )
        return text_with_meta
