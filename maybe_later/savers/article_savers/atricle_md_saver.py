from pathlib import Path

from .article_saver import ArticleSaver


class ArticleMdSaver(ArticleSaver):
    @property
    def folder_path(self) -> Path:
        folder_path = self.app_config.data_dir
        if self.article.category:
            folder_path = folder_path.joinpath(self.article.category)
            if self.article.subcategory:
                folder_path = folder_path.joinpath(self.article.subcategory)
        folder_path = folder_path.joinpath(self.article.title)
        return folder_path

    def save(self) -> None:
        pass
