import asyncio
import functools
import json

from pathlib import Path
from typing import AsyncGenerator, List

import aiofiles

from maybe_later.db.models import Meta
from maybe_later.savers import MetaModel


def make_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


def get_tags(raw_tags: str) -> List[str]:
    tags = raw_tags.split(",")
    filtered_tags = [tag.strip() for tag in tags]
    filtered_tags = [i for i in filtered_tags if i != ""]
    return filtered_tags


async def get_metas_from_folders(data_dir: Path) -> AsyncGenerator[MetaModel, None]:
    for i in data_dir.rglob("*"):
        if i.is_dir() or i.suffix != ".json":
            continue
        meta = await get_meta_from_json(i)
        yield meta


async def get_meta_from_json(json_file: Path) -> MetaModel:
    async with aiofiles.open(json_file, "r") as f:
        text = await f.read()
        data = json.loads(text)
        meta = MetaModel.from_dict(data)
    return meta


def generate_meta_output(metas: List[Meta]) -> str:
    output = ""
    for i in metas:
        tags = [t.name for t in i.tags]
        if len(tags) == 0:
            tags_str = ""
        else:
            tags_str = ", ".join(tags)
        category = i.category.name if i.category else ""
        row = f"{i.id} {i.title} {category} {tags_str}\n"
        output += row
    return output
