import asyncio

from typing import Optional, Tuple, Type, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar

from maybe_later.savers import MetaModel as ArticleMeta

from . import models


SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

ModelsWithName = Union[models.Tag, models.Category]


async def add_new_meta(article_meta: ArticleMeta, db_uri: str):
    await models.init_db(db_uri)
    meta = None
    category = await get_category(article_meta.category, db_uri)
    subcategory = None
    tags = None
    print(category)


async def get_category(
    category_name: Optional[str], db_uri: str
) -> Optional[models.Category]:
    if category_name is None:
        return None
    engine = models.get_engine(db_uri)
    async with AsyncSession(engine) as session:
        stmt = select(models.Category).where(models.Category.name == category_name)
        res = await session.execute(stmt)
        category = res.scalar()
        if category is not None:
            return category
        category = models.Category(name=category_name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
    return category
