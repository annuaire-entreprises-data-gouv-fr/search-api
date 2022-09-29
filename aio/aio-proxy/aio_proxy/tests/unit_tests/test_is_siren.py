import pytest
from aio_proxy.search.helpers import (
    is_siren,
)


@pytest.mark.parametrize(
    "siren, expected",
    [
        ("123456789", True),
        ("123 456 689", True),
        (None, None),
        ("mother of dragons", False),
        ("12345678", False),
    ],
)
def test_is_siren(siren: str, expected: boolean):
    assert is_siren(siren) == expected
