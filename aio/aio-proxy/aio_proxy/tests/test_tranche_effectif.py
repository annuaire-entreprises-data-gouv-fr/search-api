import index
import parameters
import pytest
import requests
from typing import Tuple, Any


@pytest.mark.parametrize("tranche_effectif_salarie_entreprise, expected",
                         [("NN", "NN"),
                          ("11", "11"),
                          (None, None)])
def test_parse_and_validate_tranche_effectif_salarie_entreprise(
        tranche_effectif_salarie_entreprise: str, expected: str):
    assert parameters.parse_and_validate_tranche_effectif_salarie_entreprise(
        tranche_effectif_salarie_entreprise) == expected


@pytest.mark.parametrize("tranche_effectif_salarie_entreprise", ["000000", "0"])
def test_parse_and_validate_tranche_effectif_salarie_entreprise_fail_1(
        tranche_effectif_salarie_entreprise: str):
    with pytest.raises(ValueError, match="Tranche salariés doit contenir 2 "
                                         "caractères."):
        parameters.parse_and_validate_tranche_effectif_salarie_entreprise(
            tranche_effectif_salarie_entreprise)


@pytest.mark.parametrize("tranche_effectif_salarie_entreprise", ["54", "AN"])
def test_parse_and_validate_tranche_effectif_salarie_entreprise_fail_2(
        tranche_effectif_salarie_entreprise: str):
    with pytest.raises(ValueError, match="Tranche salariés non valide."):
        parameters.parse_and_validate_tranche_effectif_salarie_entreprise(
            tranche_effectif_salarie_entreprise)
