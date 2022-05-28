import asyncio

import click

from maybe_later.config import Config
from maybe_later.downloaders import get_article
from maybe_later.savers import ArticleMdSaver as ArticleSaver

from . import utils


@click.group()
@utils.make_sync
async def main():
    pass


@main.command(help="Download an article from a given URL")
@click.option("-u", "--url", type=str, help="Article's URL")
@click.option(
    "-c",
    "--category",
    type=str,
    default="",
    help="Category and subcategory for the article. Could be in the form of 'category/subcategory' or just 'category'",
)
@click.option(
    "-t",
    "--tags",
    default="",
    type=str,
    help="Comma-separated list of tags for the article. Could be in the form of 'tag1,tag2,tag3' or just 'tag1'",
)
@utils.make_sync
async def add(url: str, category: str, tags: str):
    main_category, subcategory = utils.get_categories(category)
    article_tags = utils.get_tags(tags)
    article = await get_article(
        url, category=main_category, subcategory=subcategory, tags=article_tags
    )
    app_config = Config.from_file()
    article_saver = ArticleSaver(article, app_config)

    saving_tasks = [article_saver.save(), article_saver.save_meta()]
    res = await asyncio.gather(*saving_tasks)
    print(40 * ">")
    print(res)
