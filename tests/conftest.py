from pathlib import Path

import pytest

from maybe_later import Config, models
from maybe_later.savers.article_savers import ArticleMdSaver


@pytest.fixture
def base_dir() -> Path:
    return Path(__file__).resolve().parent


@pytest.fixture()
def config(base_dir: Path) -> Config:
    config_file = base_dir.joinpath("test_config.yaml")
    return Config.from_file(config_file)


@pytest.fixture()
def article() -> models.Article:
    return models.Article(
        title="Test title",
        text="Test text",
        source="Test source",
        category="Test category",
        subcategory="Test subcategory",
        tags=["Test tag"],
        article_html="Test article html",
    )


@pytest.fixture()
def article_md_saver(article: models.Article, config: Config) -> ArticleMdSaver:
    return ArticleMdSaver(article, config)
