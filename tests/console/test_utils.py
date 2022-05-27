from typing import List, Optional, Tuple

import pytest

from maybe_later.console import utils


@pytest.mark.parametrize(
    "input_string,expected",
    [
        ("", (None, None)),
        ("category/subcategory", ("category", "subcategory")),
        ("category/subcategory ", ("category", "subcategory")),
        ("category/subcategory/subsubcategory", ("category", "subcategory")),
        ("category", ("category", None)),
        ("category/", ("category", None)),
    ],
)
def test_get_categories(
    input_string: str, expected: Tuple[Optional[str], Optional[str]]
):
    assert utils.get_categories(input_string) == expected


@pytest.mark.parametrize(
    "input_string,expected",
    [
        ("tag1,tag2", ["tag1", "tag2"]),
        ("", []),
        ("tag1", ["tag1"]),
        ("tag1, tag2, tag3", ["tag1", "tag2", "tag3"]),
        (",", []),
    ],
)
def test_get_tags(input_string: str, expected: List[str]):
    assert utils.get_tags(input_string) == expected
