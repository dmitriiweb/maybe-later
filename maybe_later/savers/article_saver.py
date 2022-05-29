from abc import ABC, abstractmethod

from maybe_later import config

from . import models


class ArticleSaver(ABC):
    def __init__(self, article: models.ArticleModel, app_config: config.Config) -> None:
        self.article = article
        self.app_config = app_config

    @abstractmethod
    async def save(self) -> None:
        ...

    @abstractmethod
    async def save_meta(self) -> None:
        ...
