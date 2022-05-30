import asyncio

from typing import Optional, Type, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar

from maybe_later.savers import MetaModel as ArticleMeta

from . import models


SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

UniqueModels = Union[models.Tag, models.Category]


async def add_new_meta(article_meta: ArticleMeta, db_uri: str):
    await models.init_db(db_uri)
    tags_tasks = [get_tag(i, db_uri) for i in article_meta.tags]
    tags = await asyncio.gather(*tags_tasks)
    print(f"{tags=}")


async def get_tag(tag_name: str, db_uri: str) -> models.Tag:

    engine = models.get_engine(db_uri)

    async with AsyncSession(engine) as session:
        tag = await _get_by_name(tag_name, session, models.Tag)

    if tag is not None:
        return tag

    tag = models.Tag(name=tag_name)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


async def get_category(category_name: str, db_uri: str) -> models.Category:
    session = await models.get_session(db_uri)


async def _get_by_name(
    name: str, session: AsyncSession, model: Type[UniqueModels]
) -> Optional[UniqueModels]:
    stmt = select(model).where(model.name == name)
    db_res = await session.execute(stmt)
    res = db_res.first()
    return res
