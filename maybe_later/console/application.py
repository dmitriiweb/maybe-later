import click

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
    help="Category and subcategory for the article. Could be in the form of 'category/subcategory' or just 'category'",
)
@click.option(
    "-t",
    "--tags",
    type=str,
    help="Comma-separated list of tags for the article. Could be in the form of 'tag1,tag2,tag3' or just 'tag1'",
)
@utils.make_sync
async def add(url: str, category: str, tags: str):
    main_category, subcategory = utils.get_categories(category)
    article_tags = utils.get_tags(tags)
