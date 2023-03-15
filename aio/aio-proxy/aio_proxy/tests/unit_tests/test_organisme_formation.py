import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field


@pytest.mark.parametrize(
    "est_organisme_formation, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_est_organisme_formation(est_organisme_formation, expected):
    assert validate_bool_field("est_organisme_formation", est_organisme_formation) == expected


@pytest.mark.parametrize("est_organisme_formation", ["NON", "OUI", "NO", "YES"])
def test_validate_est_organisme_formation_fail(
    est_organisme_formation: str,
):
    with pytest.raises(
        ValueError,
        match="est_organisme_formation doit prendre la valeur 'true' ou 'false' !",
    ):
        validate_bool_field("est_organisme_formation", est_organisme_formation)
