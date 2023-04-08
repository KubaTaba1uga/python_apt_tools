import pytest

from app.str_utils import is_in_str


@pytest.mark.parametrize(
    "look_for, search_threw, expected", [("abc", "123abc123", True)]
)
def test_is_in_str(look_for, search_threw, expected):

    received = is_in_str(look_for, search_threw)

    assert received == expected
