import asyncio

from typing import Optional, Type, Union

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
    tags_tasks = [
        get_model_by_name_or_create(i, models.Tag, db_uri) for i in article_meta.tags
    ]
    tags = await asyncio.gather(*tags_tasks)
    print(f"{tags=}")


async def get_model_by_name_or_create(
    name: str, model: Type[ModelsWithName], db_uri: str
) -> ModelsWithName:
    engine = models.get_engine(db_uri)
    async with AsyncSession(engine) as session:
        stmt = select(model).where(model.name == name)
        db_res = await session.execute(stmt)
        res = db_res.first()
        if res is not None:
            return res  # type: ignore
        m = model(name=name)
        session.add(m)
        await session.commit()
        await session.refresh(m)
        return m
