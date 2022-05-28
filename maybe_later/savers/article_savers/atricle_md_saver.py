from maybe_later import config, models

from .article_saver import ArticleSaver


class ArticleMdSaver(ArticleSaver):
    def save(self) -> None:
        pass
