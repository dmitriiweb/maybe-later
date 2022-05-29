from typing import Optional, Type, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar

from . import models


SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

UniqueModels = Union[models.Tag, models.Category]


async def get_tag(tag_name: str, db_uri: str) -> models.Tag:
    session = await models.get_session(db_uri)
    async with session as s:

        tag = await _get_by_name(tag_name, s, models.Tag)
        if tag is not None:
            return tag

        tag = models.Tag(name=tag_name)
        s.add(tag)
        await s.commit()
        await s.refresh(tag)
    return tag


async def get_category(category_name: str, db_uri: str) -> models.Category:
    session = await models.get_session(db_uri)
    async with session as s:
        pass


async def _get_by_name(
    name: str, session: AsyncSession, model: Type[UniqueModels]
) -> Optional[UniqueModels]:
    stmt = select(model).where(model.name == name)
    db_res = await session.execute(stmt)
    res = db_res.first()
    return res
