import pytest
from aio_proxy.parsers.entrepreneur_individuel import (
    validate_is_entrepreneur_individuel,
)


@pytest.mark.parametrize(
    "est_entrepreneur_individuel, expected", [("TRUE", True), ("False", False), (None,
                                                                             None)]
)
def test_validate_is_entrepreneur_individuel(
    is_entrepreneur_individuel: str, expected: str
):
    assert validate_is_entrepreneur_individuel(is_entrepreneur_individuel) == expected


@pytest.mark.parametrize("est_entrepreneur_individuel", ["NON", "OUI"])
def test_validate_is_entrepreneur_individuel_fail(
    is_entrepreneur_individuel: str,
):
    with pytest.raises(
        ValueError,
            match="est_entrepreneur_spectacle doit prendre la valeur 'true' "
                  "or 'false' !",
    ):
        validate_is_entrepreneur_individuel(is_entrepreneur_individuel)
