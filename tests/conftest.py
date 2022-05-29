from pathlib import Path

import pytest

from maybe_later import Config
from maybe_later.savers import ArticleMdSaver, ArticleModel, MetaModel


@pytest.fixture
def base_dir() -> Path:
    return Path(__file__).resolve().parent


@pytest.fixture()
def article_html(base_dir: Path) -> str:
    html_file = base_dir.joinpath("data_files_for_tests", "article.html")
    with open(html_file) as f:
        return f.read()


@pytest.fixture()
def config(base_dir: Path) -> Config:
    config_file = base_dir.joinpath("test_config.yaml")
    return Config.from_file(config_file)


@pytest.fixture()
def article(article_html: str) -> ArticleModel:
    meta = MetaModel(
        title="Test title",
        source="Test source",
        category="Test category",
        subcategory="Test subcategory",
        tags=["Test tag"],
    )
    return ArticleModel(text="Test text", article_html=article_html, meta=meta)


@pytest.fixture()
def article_md_saver(article: ArticleModel, config: Config) -> ArticleMdSaver:
    return ArticleMdSaver(article, config)
