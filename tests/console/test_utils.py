from typing import List

import pytest

from maybe_later.console import utils


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
