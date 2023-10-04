import pytest
from aio_proxy.request.helpers import str_to_list


@pytest.mark.parametrize(
    "string, expected",
    [("GE,PME", ["GE", "PME"]), ("N", ["N"])],
)
def test_str_to_list(string, expected):
    assert str_to_list(string) == expected
