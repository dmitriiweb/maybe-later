from typing import List, Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, Relationship, SQLModel


class MetaTagLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    meta_id: Optional[int] = Field(
        default=None, foreign_key="meta.id", primary_key=True
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(sa_column_kwargs={"unique": True})

    metas: List["Meta"] = Relationship(back_populates="tags", link_model=MetaTagLink)


class Meta(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    title: str = Field(sa_column_kwargs={"unique": True})
    source: str
    status: int

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(
        back_populates="metas", sa_relationship_kwargs={"lazy": "joined"}
    )

    tags: List[Tag] = Relationship(
        back_populates="metas",
        link_model=MetaTagLink,
        sa_relationship_kwargs={"lazy": "joined"},
    )


class Category(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(sa_column_kwargs={"unique": True})

    metas: List[Meta] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "joined"},
    )


async def init_db(db_url: str) -> None:
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_engine(db_connection_string: str):
    return create_async_engine(db_connection_string)
