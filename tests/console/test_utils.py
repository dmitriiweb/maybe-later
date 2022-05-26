from typing import Optional, Tuple

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
