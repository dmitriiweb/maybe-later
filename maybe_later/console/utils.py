import asyncio
import functools

from typing import List, Optional, Tuple


def make_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


def get_categories(raw_categories: str) -> Tuple[Optional[str], Optional[str]]:
    raw_categories = raw_categories.strip()
    cats = raw_categories.split("/")
    filtered_cats = [cat.strip() if cat != "" else None for cat in cats]
    total_cats = len(filtered_cats)
    if total_cats == 0:
        return None, None
    elif total_cats == 1:
        return filtered_cats[0], None
    return filtered_cats[0], filtered_cats[1]


def get_tags(raw_tags: str) -> List[str]:
    tags = raw_tags.split(",")
    filtered_tags = [tag.strip() for tag in tags]
    filtered_tags = [i for i in filtered_tags if i != ""]
    return filtered_tags
