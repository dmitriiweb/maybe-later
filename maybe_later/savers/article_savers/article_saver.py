from abc import ABC, abstractmethod

from maybe_later import config, models


class ArticleSaver(ABC):
    def __init__(self, article: models.Article, app_config: config.Config) -> None:
        self.article = article
        self.app_config = app_config

    @abstractmethod
    async def save(self) -> None:
        ...
