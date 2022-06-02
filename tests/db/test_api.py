from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from maybe_later.db.models import Meta, get_engine


async def test_add_new_meta(add_new_meta_to_db, base_dir):
    sqlite_path = str(base_dir.joinpath("db.sqlite3").absolute())
    connection_string = f"sqlite+aiosqlite:///{sqlite_path}"
    engine = get_engine(connection_string)

    async with AsyncSession(engine) as session:
        stmt = select(Meta).where(Meta.id == 1)
        res = await session.execute(stmt)
        meta: Meta = res.scalar()

    meta_tags = [i.name for i in meta.tags]
    sub_categories = [i.name for i in meta.category.subcategories]

    assert meta.title == "Test title"
    assert meta.category.name == "Test category"
    assert "Test subcategory" in sub_categories
    assert "Test tag" in meta_tags
