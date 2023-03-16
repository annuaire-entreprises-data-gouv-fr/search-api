import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field


@pytest.mark.parametrize(
    "egapro_renseignee, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_egapro_renseignee(egapro_renseignee, expected):
    assert validate_bool_field("egapro_renseignee", egapro_renseignee) == expected


@pytest.mark.parametrize("egapro_renseignee", ["NON", "OUI", "NO", "YES"])
def test_validate_egapro_renseignee_fail(
    egapro_renseignee: str,
):
    with pytest.raises(
        ValueError,
        match="egapro_renseignee doit prendre la valeur 'true' ou 'false' !",
    ):
        validate_bool_field("egapro_renseignee", egapro_renseignee)
