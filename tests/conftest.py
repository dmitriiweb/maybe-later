from pathlib import Path

import pytest

from maybe_later import Config
from maybe_later.db.api import add_new_meta
from maybe_later.db.models import init_db
from maybe_later.savers import ArticleMdSaver, ArticleModel, MetaModel
from maybe_later.savers.models import ArticleStatus


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
        tags=["Test tag"],
        status=ArticleStatus.UNREAD,
    )
    return ArticleModel(text="Test text", article_html=article_html, meta=meta)


@pytest.fixture()
def article_md_saver(article: ArticleModel, config: Config) -> ArticleMdSaver:
    return ArticleMdSaver(article, config)


@pytest.fixture()
async def add_new_meta_to_db(article: ArticleModel, config: Config, base_dir: Path):
    db_file_name = "db.sqlite3"
    fb_file_path = base_dir.joinpath(db_file_name)
    config.data_dir = base_dir

    await init_db(config.db_uri)
    await add_new_meta(article.meta, config.db_uri)

    yield

    fb_file_path.unlink()
