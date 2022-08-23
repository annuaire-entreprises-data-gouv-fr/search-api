import pytest
from aio_proxy.parsers.entrepreneur_individuel import (
    validate_is_entrepreneur_individuel,
)


@pytest.mark.parametrize(
    "is_entrepreneur_individuel, expected", [("YES", True), ("NO", False), (None, None)]
)
def test_validate_is_entrepreneur_individuel(
    is_entrepreneur_individuel: str, expected: str
):
    assert validate_is_entrepreneur_individuel(is_entrepreneur_individuel) == expected


@pytest.mark.parametrize("is_entrepreneur_individuel", ["NON", "OUI"])
def test_validate_is_entrepreneur_individuel_fail(
    is_entrepreneur_individuel: str,
):
    with pytest.raises(
        ValueError,
        match="Seuls les valeurs 'yes' ou bien 'no' sont "
        "possibles pour "
        "'is_entrepreneur_individuel'.",
    ):
        validate_is_entrepreneur_individuel(is_entrepreneur_individuel)
