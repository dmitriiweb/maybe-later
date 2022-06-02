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
NonTagModel = Union[models.Category, models.SubCategory, models.Meta]


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
        tag = res.scalar()
    if tag is not None:
        return tag
    tag = models.Tag(name=tag_name)
    await save_model_to_db(tag, db_uri)
    return tag


async def get_subcategory(
    category: Optional[models.Category],
    sub_category_name: Optional[str],
    db_uri: str,
) -> Optional[models.SubCategory]:
    if sub_category_name is None or category is None:
        return None
    engine = models.get_engine(db_uri)
    async with AsyncSession(engine) as session:
        stmt = (
            select(models.SubCategory)
            .where(models.SubCategory.category_id == category.id)
            .where(models.SubCategory.name == sub_category_name)
        )

        res = await session.execute(stmt)
        subcategory = res.scalar()
    if subcategory is not None:
        return subcategory
    subcategory = models.SubCategory(name=sub_category_name, category_id=category.id)
    await save_model_to_db(subcategory, db_uri)
    category.subcategories.append(subcategory)
    return subcategory


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
    await save_model_to_db(category, db_uri)
    return category
