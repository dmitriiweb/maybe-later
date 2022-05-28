from abc import ABC, abstractmethod

from maybe_later import config, models


class ArticleSaver(ABC):
    def __int__(
        self, article: models.Article, *, app_config: config.Config, **kwargs
    ) -> None:
        self.article = article
        self.app_config = app_config

    @abstractmethod
    def save(self) -> None:
        ...
