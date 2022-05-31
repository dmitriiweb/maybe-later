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


async def get_tag(tag_name: str, session: AsyncSession) -> models.Tag:
    pass


async def get_subcategory(
    category: Optional[models.Category],
    sub_category_name: Optional[str],
    session: AsyncSession,
) -> Optional[models.SubCategory]:
    if sub_category_name is None or category is None:
        return None
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
    category.subcategories.append(subcategory)
    session.add(subcategory)
    session.add(category)
    await session.commit()
    await session.refresh(subcategory)
    await session.refresh(category)
    return subcategory


async def get_category(
    category_name: Optional[str], session: AsyncSession
) -> Optional[models.Category]:
    if category_name is None:
        return None
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
