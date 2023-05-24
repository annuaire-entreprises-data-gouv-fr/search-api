import pytest
from aio_proxy.request.parsers.rge import validate_id_rge


@pytest.mark.parametrize(
    "id_rge, expected",
    [("8621T18D109", "8621T18D109"), ("1", "1"), (None, None)],
)
def test_validate_id_rge(id_rge, expected):
    assert validate_id_rge(id_rge) == expected
