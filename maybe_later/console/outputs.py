from typing import List

from tabulate import tabulate
from termcolor import colored

from maybe_later._types import ArticleStatus
from maybe_later.db.models import Meta


def print_output(output: List[List[str]]) -> None:
    print()
    print(tabulate(output, headers="firstrow"))
    print()


def string_shorter(text: str, max_length: int = 50) -> str:
    if len(text) <= max_length:
        return text
    return f"{text[:max_length]}..."


def color_text(text: str, color: str) -> str:
    res: str = colored(text, color)
    return res


def color_factory(status: ArticleStatus):
    colors = {
        ArticleStatus.UNREAD: "green",
        ArticleStatus.READ: "gray",
        ArticleStatus.IMPORTANT: "red",
    }
    try:
        return colors[status]
    except KeyError:
        raise ValueError(f"Unknown status: {status}")


def make_meta_row(meta: Meta) -> List[str]:
    tags = [t.name for t in meta.tags]
    if len(tags) == 0:
        tags_str = ""
    else:
        tags_str = ", ".join(tags)
    category = meta.category.name if meta.category else ""
    row = [str(meta.id), string_shorter(meta.title), category, string_shorter(tags_str)]
    row_color = color_factory(ArticleStatus(meta.status))
    row = [color_text(r, row_color) for r in row]
    return row


def generate_meta_output(metas: List[Meta]) -> List[List[str]]:
    output = [["ID", "Title", "Category", "Tags"]]
    for i in metas:
        row = make_meta_row(i)
        output.append(row)
    return output
