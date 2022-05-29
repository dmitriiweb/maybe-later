import asyncio

from maybe_later.config import Config
from maybe_later.savers import MetaModel as ArticleMeta

from . import models, services


async def add_new_meta(article_meta: ArticleMeta, app_config: Config):
    await models.init_db(app_config.db_uri)
    tags_tasks = [services.get_tag(i, app_config.db_uri) for i in article_meta.tags]
    tags = await asyncio.gather(*tags_tasks)
    print(f"{tags=}")
