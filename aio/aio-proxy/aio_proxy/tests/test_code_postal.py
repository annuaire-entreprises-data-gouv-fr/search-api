import parameters
import pytest


@pytest.mark.parametrize("code_postal, expected", [("45000", "45000"), (None, None)])
def test_validate_code_postal(code_postal: str, expected: str):
    assert parameters.validate_code_postal(code_postal) == expected


@pytest.mark.parametrize("code_postal", ["4500", "0"])
def test_validate_code_postal_fail_1(code_postal: str):
    with pytest.raises(ValueError, match="Code postal doit contenir 5 caractères !"):
        parameters.validate_code_postal(code_postal)


@pytest.mark.parametrize("code_postal", ["45A90", "AAAAA"])
def test_validate_code_postal_fail_2(code_postal: str):
    with pytest.raises(ValueError, match="Code postal non valide."):
        parameters.validate_code_postal(code_postal)
