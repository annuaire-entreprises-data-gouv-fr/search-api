import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field


@pytest.mark.parametrize(
    "est_bio, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_est_bio(est_bio, expected):
    assert validate_bool_field("est_bio", est_bio) == expected


@pytest.mark.parametrize("est_bio", ["NON", "OUI", "NO", "YES"])
def test_validate_est_bio_fail(
    est_bio: str,
):
    with pytest.raises(
        ValueError,
        match="est_bio doit prendre la valeur 'true' ou 'false' !",
    ):
        validate_bool_field("est_bio", est_bio)
