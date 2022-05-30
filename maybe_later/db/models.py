from datetime import datetime
from typing import AsyncGenerator, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Relationship, SQLModel


class MetaTagLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    meta_id: Optional[int] = Field(
        default=None, foreign_key="meta.id", primary_key=True
    )


class TagCategoryLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", primary_key=True
    )


class TagSubCategoryLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    subcategory_id: Optional[int] = Field(
        default=None, foreign_key="subcategory.id", primary_key=True
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(sa_column_kwargs={"unique": True})

    metas: List["Meta"] = Relationship(back_populates="tags", link_model=MetaTagLink)
    categories: List["Category"] = Relationship(
        back_populates="tags", link_model=TagCategoryLink
    )
    subcategories: List["SubCategory"] = Relationship(
        back_populates="tags", link_model=TagSubCategoryLink
    )


class SubCategory(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="subcategories")
    tags: List[Tag] = Relationship(
        back_populates="subcategories", link_model=TagSubCategoryLink
    )


class Category(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(sa_column_kwargs={"unique": True})

    subcategories: List[SubCategory] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    meta_id: Optional[int] = Field(default=None, foreign_key="meta.id")
    meta: Optional["Meta"] = Relationship(back_populates="category")
    tags: List[Tag] = Relationship(
        back_populates="categories", link_model=TagCategoryLink
    )


class Meta(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    title: str
    source: str
    category: Optional[Category] = Relationship(
        back_populates="meta",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False},
    )
    tags: List[Tag] = Relationship(back_populates="metas", link_model=MetaTagLink)
    created_at: Optional[datetime]


async def init_db(db_url: str) -> None:
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_engine(db_connection_string: str):
    return create_async_engine(db_connection_string)
