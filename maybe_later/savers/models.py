from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "source": self.source,
            "category": self.category,
            "subcategory": self.subcategory,
            "tags": self.tags,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetaModel":
        return cls(
            title=data["title"],
            source=data["source"],
            category=data["category"],
            subcategory=data["subcategory"],
            tags=data["tags"],
            status=ArticleStatus(data["status"]),
        )


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
