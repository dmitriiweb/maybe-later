from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class SubCategory(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="subcategories")


class Category(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str

    subcategories: List[SubCategory] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    meta_id: Optional[int] = Field(default=None, foreign_key="meta.id")
    meta: Optional["Meta"] = Relationship(back_populates="category")


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str


class Meta(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    title: str
    source: str
    category: Optional[Category] = Relationship(
        back_populates="meta",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False},
    )
