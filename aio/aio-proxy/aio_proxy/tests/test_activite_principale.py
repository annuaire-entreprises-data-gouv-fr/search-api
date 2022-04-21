import index
import parameters
import pytest
import requests
from typing import Tuple, Any


@pytest.mark.parametrize(
    "activite_principale, expected",
    [("62.01Z", "62.01Z"), ("27.33Z", "27.33Z"), (None, None)],
)
def test_parse_and_validate_activite_principale(activite_principale, expected):
    assert (
        parameters.parse_and_validate_activite_principale(activite_principale)
        == expected
    )


@pytest.mark.parametrize("activite_principale", ["11111", "2733Z"])
def test_parse_and_validate_activite_principale_fail_1(activite_principale: str):
    with pytest.raises(
        ValueError, match="Activité principale doit contenir 6 " "caractères."
    ):
        parameters.parse_and_validate_activite_principale(activite_principale)


@pytest.mark.parametrize("activite_principale", ["27.33A"])
def test_parse_and_validate_activite_principale_fail_2(activite_principale: str):
    with pytest.raises(ValueError, match="Activité principale inconnue."):
        parameters.parse_and_validate_activite_principale(activite_principale)
