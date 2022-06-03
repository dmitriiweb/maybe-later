from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from maybe_later.db import api
from maybe_later.db.models import Meta, get_engine


async def test_add_new_meta(add_new_meta_to_db, base_dir, article):
    sqlite_path = str(base_dir.joinpath("db.sqlite3").absolute())
    connection_string = f"sqlite+aiosqlite:///{sqlite_path}"
    engine = get_engine(connection_string)

    async with AsyncSession(engine) as session:
        stmt = select(Meta).where(Meta.title == article.meta.title)
        res = await session.execute(stmt)
        meta: Meta = res.scalar()

    meta_tags = [i.name for i in meta.tags]

    assert meta.title == article.meta.title
    assert meta.category.name == article.meta.category
    assert "Test tag" in meta_tags


async def test_get_metas(add_new_meta_to_db, base_dir, article):
    sqlite_path = str(base_dir.joinpath("db.sqlite3").absolute())
    connection_string = f"sqlite+aiosqlite:///{sqlite_path}"

    metas = await api.get_metas(connection_string)
    meta = metas[0]

    assert len(metas) == 1
    assert meta.title == article.meta.title
