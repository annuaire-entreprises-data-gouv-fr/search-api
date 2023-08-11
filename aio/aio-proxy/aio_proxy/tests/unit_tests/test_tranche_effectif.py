import pytest
from aio_proxy.request.parsers.tranche_effectif import (
    validate_tranche_effectif_salarie,
)


@pytest.mark.parametrize(
    "tranche_effectif_salarie, expected",
    [(["NN", "11"], ["NN", "11"]), ([], [])],
)
def test_validate_tranche_effectif_salarie(
    tranche_effectif_salarie: list[str], expected: list[str]
):
    assert validate_tranche_effectif_salarie(tranche_effectif_salarie) == expected


@pytest.mark.parametrize("tranche_effectif_salarie", [["000000", "0"]])
def test_validate_tranche_effectif_salarie_fail_1(
    tranche_effectif_salarie: list[str],
):
    with pytest.raises(
        ValueError, match="Chaque tranche salariés doit contenir 2 caractères."
    ):
        validate_tranche_effectif_salarie(tranche_effectif_salarie)


@pytest.mark.parametrize("tranche_effectif_salarie", [["54", "AN"]])
def test_validate_tranche_effectif_salarie_fail_2(
    tranche_effectif_salarie: list[str],
):
    with pytest.raises(
        ValueError, match="Au moins une tranche " "salariés est non valide."
    ):
        validate_tranche_effectif_salarie(tranche_effectif_salarie)
