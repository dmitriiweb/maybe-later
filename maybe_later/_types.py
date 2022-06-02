from enum import Enum, auto


class ArticleStatus(Enum):
    UNREAD = auto()
    READ = auto()
    IMPORTANT = auto()
