from typing import Any, Tuple

import index
import parameters
import pytest
import requests


@pytest.mark.parametrize(
    "is_entrepreneur_individuel, expected", [("YES", True), ("NO", False), (None, None)]
)
def test_parse_and_validate_is_entrepreneur_individuel(
    is_entrepreneur_individuel: str, expected: str
):
    assert (
        parameters.parse_and_validate_is_entrepreneur_individuel(
            is_entrepreneur_individuel
        )
        == expected
    )


@pytest.mark.parametrize("is_entrepreneur_individuel", ["NON", "OUI"])
def test_parse_and_validate_is_entrepreneur_individuel_fail(
    is_entrepreneur_individuel: str,
):
    with pytest.raises(
        ValueError,
        match="Seuls les valeurs 'yes' ou bien 'no' sont "
        "possibles pour "
        "'is_entrepreneur_individuel'.",
    ):
        parameters.parse_and_validate_is_entrepreneur_individuel(
            is_entrepreneur_individuel
        )
