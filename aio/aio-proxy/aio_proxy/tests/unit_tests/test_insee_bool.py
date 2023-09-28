import pytest
from aio_proxy.request.helpers import match_bool_to_insee_value


@pytest.mark.parametrize(
    "bool, expected",
    [(True, "O"), (False, "N")],
)
def test_match_bool_to_insee_value(bool, expected):
    assert match_bool_to_insee_value(bool) == expected
