import asyncio

from typing import Optional

import click

from sqlalchemy.exc import IntegrityError
from tabulate import tabulate

from maybe_later.config import Config
from maybe_later.db import api
from maybe_later.downloaders import get_article
from maybe_later.savers import ArticleMdSaver as ArticleSaver

from . import outputs, utils


@click.group()
@utils.make_sync
async def main():
    pass


@main.command(help="Download an article from a given URL")
@click.option("-u", "--url", type=str, help="Article's URL")
@click.option("-c", "--category", type=str, default="", help="Category for the article")
@click.option(
    "-t",
    "--tags",
    default="",
    type=str,
    help="Comma-separated list of tags for the article. Could be in the form of 'tag1,tag2,tag3' or just 'tag1'",
)
@utils.make_sync
async def add(url: str, category: str, tags: str):
    article_tags = utils.get_tags(tags)
    article = await get_article(url, category=category, tags=article_tags)
    app_config = Config.from_file()
    article_saver = ArticleSaver(article, app_config)

    saving_tasks = [
        article_saver.save(),
        article_saver.save_meta(),
        api.add_new_meta(article.meta, app_config.db_uri),
    ]
    try:
        await asyncio.gather(*saving_tasks)
    except IntegrityError:
        print(f'Article "{article.meta.title}" already exists in the database')


@main.command(help="Recreate DB with articles' metas")
@utils.make_sync
async def update():
    app_config = Config.from_file()
    app_config.sqlite_db_path.unlink(missing_ok=True)
    metas = utils.get_metas_from_folders(app_config.data_dir)
    async for meta in metas:
        print(f"Updating: {meta.title}")
        await api.add_new_meta(meta, app_config.db_uri),


@main.group(help="Show articles, categories and tags")
@utils.make_sync
async def show():
    pass


@show.command(help="Show all articles")
@click.option(
    "-c",
    "--categories",
    type=str,
    default=None,
    required=False,
    help="Comma-separated list of categories",
)
@utils.make_sync
async def articles(categories: Optional[str]):
    show_categories = None if categories is None else categories.split(",")
    app_config = Config.from_file()
    metas = await api.get_metas(app_config.db_uri, show_categories)
    output = outputs.generate_meta_output(metas)
    print(tabulate(output, headers="firstrow"))
