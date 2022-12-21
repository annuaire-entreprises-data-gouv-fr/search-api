import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field


@pytest.mark.parametrize(
    "est_entrepreneur_spectacle, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_est_entrepreneur_spectacle(est_entrepreneur_spectacle, expected):
    assert (
        validate_bool_field("est_entrepreneur_spectacle", est_entrepreneur_spectacle)
        == expected
    )


@pytest.mark.parametrize("est_entrepreneur_spectacle", ["NON", "OUI", "NO", "YES"])
def test_validate_est_entrepreneur_spectacle_fail(
    est_entrepreneur_spectacle: str,
):
    with pytest.raises(
        ValueError,
        match="est_entrepreneur_spectacle doit prendre la valeur 'true' "
        "ou 'false' !",
    ):
        validate_bool_field("est_entrepreneur_spectacle", est_entrepreneur_spectacle)
