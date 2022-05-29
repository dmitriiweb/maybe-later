import json

from pathlib import Path

import aiofiles

from .article_saver import ArticleSaver


class ArticleMdSaver(ArticleSaver):
    @property
    def folder_path(self) -> Path:
        folder_path = self.app_config.data_dir
        if self.article.meta.category:
            folder_path = folder_path.joinpath(self.article.meta.category)
            if self.article.meta.subcategory:
                folder_path = folder_path.joinpath(self.article.meta.subcategory)
        folder_path = folder_path.joinpath(self.article.meta.title)
        return folder_path

    @property
    def md_file_path(self) -> Path:
        return self.folder_path.joinpath(self.article.meta.title + ".md")

    @property
    def meta_file_path(self) -> Path:
        return self.folder_path.joinpath(self.article.meta.title + ".json")

    async def save(self) -> None:
        self.folder_path.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(self.md_file_path, "w") as f:
            await f.write(self.article.to_markdown())

    async def save_meta(self) -> None:
        meta = {
            "title": self.article.meta.title,
            "source": self.article.meta.source,
            "category": self.article.meta.category,
            "subcategory": self.article.meta.subcategory,
            "tags": self.article.meta.tags,
            "status": self.article.meta.status.value,
        }
        meta_json = json.dumps(meta)
        async with aiofiles.open(self.meta_file_path, "w") as f:
            await f.write(meta_json)
