import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field
from aio_proxy.parsers.uai import validate_id_uai


@pytest.mark.parametrize(
    "est_uai, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_est_uai(est_uai, expected):
    assert validate_bool_field("est_uai", est_uai) == expected


@pytest.mark.parametrize("est_uai", ["NON", "OUI", "NO", "YES"])
def test_validate_est_uai_fail(
    est_uai: str,
):
    with pytest.raises(
        ValueError,
        match="est_uai doit prendre la valeur 'true' ou 'false' !",
    ):
        validate_bool_field("est_uai", est_uai)


@pytest.mark.parametrize(
    "id_uai, expected",
    [("0022008X", "0022008X"), ("0750999D", "0750999D"), (None, None)],
)
def test_validate_id_uai(id_uai, expected):
    assert validate_id_uai(id_uai) == expected


@pytest.mark.parametrize("id_uai", ["0022008", "0022008XY"])
def test_validate_id_uai_fail(id_uai: str):
    with pytest.raises(
        ValueError, match="L'identifiant UAI doit contenir 8 caractères."
    ):
        validate_id_uai(id_uai)
