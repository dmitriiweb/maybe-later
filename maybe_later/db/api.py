import asyncio

from typing import List, Optional

from maybe_later.savers import MetaModel as ArticleMeta

from . import models, services


async def add_new_meta(article_meta: ArticleMeta, db_uri: str):
    await models.init_db(db_uri)

    category = await services.get_category(article_meta.category, db_uri)
    tag_task = [services.get_tag(tag, db_uri) for tag in article_meta.tags]
    tags = await asyncio.gather(*tag_task)
    meta = models.Meta(
        title=article_meta.title,
        category_id=category.id,
        source=article_meta.source,
        status=article_meta.status.value,
        tags=tags,
    )
    await services.save_model_to_db(meta, db_uri)


async def get_metas(
    db_uri, categories: Optional[List[str]] = None
) -> List[models.Meta]:
    if categories is None:
        metas = await services.get_metas(db_uri)
    else:
        metas = await services.get_metas_by_categories(categories, db_uri)
    return metas
