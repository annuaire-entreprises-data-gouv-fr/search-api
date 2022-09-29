import pytest
from aio_proxy.search.helpers import is_siren


@pytest.mark.parametrize(
    "siren, expected",
    [
        ("123456789", True),
        ("123 456 689", True),
        (None, False),
        ("mother of dragons", False),
        ("12345678", False),
        ("12345678900000", False)
    ],
)
def test_is_siren(siren: str, expected):
    assert is_siren(siren) == expected
