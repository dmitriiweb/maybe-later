from typing import List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar

from . import models


SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

ModelsWithName = Union[models.Tag, models.Category]
NonTagModel = Union[models.Category, models.Meta]


async def save_model_to_db(model, db_uri: str) -> None:
    engine = models.get_engine(db_uri)
    async with AsyncSession(engine) as session:
        session.add(model)
        await session.commit()
        await session.refresh(model)


async def get_tag(tag_name: str, db_uri: str) -> models.Tag:
    engine = models.get_engine(db_uri)
    async with AsyncSession(engine) as session:
        stmt = select(models.Tag).where(models.Tag.name == tag_name)
        res = await session.execute(stmt)
        tag: Optional[models.Tag] = res.scalar()
    if tag is not None:
        return tag
    tag = models.Tag(name=tag_name)
    await save_model_to_db(tag, db_uri)
    return tag


async def get_category(category_name: str, db_uri: str) -> models.Category:
    engine = models.get_engine(db_uri)
    async with AsyncSession(engine) as session:
        stmt = select(models.Category).where(models.Category.name == category_name)
        res = await session.execute(stmt)
        category: Optional[models.Category] = res.scalar()
    if category is not None:
        return category
    category = models.Category(name=category_name)
    await save_model_to_db(category, db_uri)
    return category


async def get_metas(db_uri: str) -> List[models.Meta]:
    engine = models.get_engine(db_uri)
    async with AsyncSession(engine) as session:
        stmt = select(models.Meta)
        res = await session.execute(stmt)

    metas = res.scalars().unique()
    return list(metas)


async def get_metas_by_categories(
    category_names: List[str], db_uri: str
) -> List[models.Meta]:
    engine = models.get_engine(db_uri)
    metas: List[models.Meta] = []
    async with AsyncSession(engine) as session:
        for i in category_names:
            stmt = select(models.Category).where(models.Category.name == i)
            res = await session.execute(stmt)
            category: Optional[models.Category] = res.scalar()
            if category is None:
                continue
            meta_stmt = select(models.Meta).where(
                models.Meta.category_id == category.id
            )
            res = await session.execute(meta_stmt)
            m = res.scalars().unique()
            metas.extend(m)
    return metas
