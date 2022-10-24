import pytest
from aio_proxy.parsers.code_commune import validate_code_commune


@pytest.mark.parametrize("code_commune, expected", [("02017", "02017"), (None, None)])
def test_validate_code_commune(code_commune: str, expected: str):
    assert validate_code_commune(code_commune) == expected


@pytest.mark.parametrize("code_commune", ["1A90", "0"])
def test_validate_code_commune_fail_1(code_commune: str):
    with pytest.raises(ValueError, match="Code commune doit contenir 5 caractères !"):
        validate_code_commune(code_commune)


@pytest.mark.parametrize("code_commune", ["093BA", "AAAAA"])
def test_validate_code_commune_fail_2(code_commune: str):
    with pytest.raises(ValueError, match="Code commune non valide."):
        validate_code_commune(code_commune)
