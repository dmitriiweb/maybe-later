from typing import List

from maybe_later.db.models import Meta


def generate_meta_output(metas: List[Meta]) -> List[List[str]]:
    output = [["ID", "Title", "Category", "Tags"]]
    for i in metas:
        tags = [t.name for t in i.tags]
        if len(tags) == 0:
            tags_str = ""
        else:
            tags_str = ", ".join(tags)
        category = i.category.name if i.category else ""
        row = [str(i.id), i.title, category, tags_str]
        output.append(row)
    return output
