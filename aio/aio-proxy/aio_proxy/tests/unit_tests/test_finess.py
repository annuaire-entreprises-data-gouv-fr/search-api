import pytest
from aio_proxy.request.parsers.finess import validate_id_finess


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
