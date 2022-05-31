from sqlalchemy.ext.asyncio import AsyncSession

from maybe_later.config import Config
from maybe_later.savers import MetaModel as ArticleMeta

from . import models, services


async def add_new_meta(article_meta: ArticleMeta, db_uri: str):
    await models.init_db(db_uri)
    engine = models.get_engine(db_uri)
    async with AsyncSession(engine) as session:
        meta = None
        category = await services.get_category(article_meta.category, session)
        subcategory = await services.get_subcategory(
            category, article_meta.subcategory, session
        )
        tags = None
        print(category)
        print(40 * "-")
        print(subcategory)
