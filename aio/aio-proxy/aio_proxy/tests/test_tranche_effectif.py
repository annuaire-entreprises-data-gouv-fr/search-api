import pytest
from aio_proxy.parsers.tranche_effectif import (
    validate_tranche_effectif_salarie,
)


@pytest.mark.parametrize(
    "tranche_effectif_salarie, expected",
    [("NN", "NN"), ("11", "11"), (None, None)],
)
def test_validate_tranche_effectif_salarie(
    tranche_effectif_salarie: str, expected: str
):
    assert (
        validate_tranche_effectif_salarie(
            tranche_effectif_salarie
        )
        == expected
    )


@pytest.mark.parametrize("tranche_effectif_salarie", ["000000", "0"])
def test_validate_tranche_effectif_salarie_fail_1(
    tranche_effectif_salarie: str,
):
    with pytest.raises(
        ValueError, match="Tranche salariés doit contenir 2 " "caractères."
    ):
        validate_tranche_effectif_salarie(
            tranche_effectif_salarie
        )


@pytest.mark.parametrize("tranche_effectif_salarie", ["54", "AN"])
def test_validate_tranche_effectif_salarie_fail_2(
    tranche_effectif_salarie: str,
):
    with pytest.raises(ValueError, match="Tranche salariés non valide."):
        validate_tranche_effectif_salarie(
            tranche_effectif_salarie
        )
