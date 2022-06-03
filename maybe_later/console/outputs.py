from typing import List

from tabulate import tabulate

from maybe_later.db.models import Meta


def print_output(output: List[List[str]]) -> None:
    print()
    print(tabulate(output, headers="firstrow"))
    print()


def string_shorter(text: str, max_length: int = 50) -> str:
    if len(text) <= max_length:
        return text
    return f"{text[:max_length]}..."


def generate_meta_output(metas: List[Meta]) -> List[List[str]]:
    output = [["ID", "Title", "Category", "Tags"]]
    for i in metas:
        tags = [t.name for t in i.tags]
        if len(tags) == 0:
            tags_str = ""
        else:
            tags_str = ", ".join(tags)
        category = i.category.name if i.category else ""
        row = [str(i.id), string_shorter(i.title), category, string_shorter(tags_str)]
        output.append(row)
    return output
