import index
import parameters
import pytest
import requests
from typing import Tuple, Any


@pytest.mark.parametrize("code_postal, expected", [("45000", "45000"), (None, None)])
def test_parse_and_validate_code_postal(code_postal: str, expected: str):
    assert parameters.parse_and_validate_code_postal(code_postal) == expected


@pytest.mark.parametrize("code_postal", ["4500", "0"])
def test_parse_and_validate_code_postal_fail_1(code_postal: str):
    with pytest.raises(ValueError, match="Code postal doit contenir 5 caractères !"):
        parameters.parse_and_validate_code_postal(code_postal)


@pytest.mark.parametrize("code_postal", ["45A90", "AAAAA"])
def test_parse_and_validate_code_postal_fail_2(code_postal: str):
    with pytest.raises(ValueError, match="Code postal non valide."):
        parameters.parse_and_validate_code_postal(code_postal)
