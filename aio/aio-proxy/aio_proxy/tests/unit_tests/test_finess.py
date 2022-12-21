import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field
from aio_proxy.parsers.finess import validate_id_finess


@pytest.mark.parametrize(
    "est_finess, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_est_finess(est_finess, expected):
    assert validate_bool_field("est_finess", est_finess) == expected


@pytest.mark.parametrize("est_finess", ["NON", "OUI", "NO", "YES"])
def test_validate_est_finess_fail(
    est_finess: str,
):
    with pytest.raises(
        ValueError,
        match="est_finess doit prendre la valeur 'true' ou 'false' !",
    ):
        validate_bool_field("est_finess", est_finess)


@pytest.mark.parametrize(
    "id_finess, expected",
    [("750008328", "750008328"), ("750012494", "750012494"), (None, None)],
)
def test_validate_id_finess(id_finess, expected):
    assert validate_id_finess(id_finess) == expected


@pytest.mark.parametrize("id_finess", ["00220081", "7500124944"])
def test_validate_id_finess_fail(id_finess: str):
    with pytest.raises(
        ValueError, match="L'identifiant FINESS doit contenir 9 caractères."
    ):
        validate_id_finess(id_finess)
