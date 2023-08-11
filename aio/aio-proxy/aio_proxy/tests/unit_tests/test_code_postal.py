import pytest
from aio_proxy.request.parsers.code_postal import validate_code_postal


@pytest.mark.parametrize(
    "code_postal, expected",
    [(["45000", "69000"], ["45000", "69000"]), ([], [])],
)
def test_validate_code_postal(code_postal: list[str], expected: list[str]):
    assert validate_code_postal(code_postal) == expected


@pytest.mark.parametrize("code_postal", [["4500", "0"]])
def test_validate_code_postal_fail_1(code_postal: list[str]):
    with pytest.raises(
        ValueError, match="Chaque code postal doit contenir 5 caractères !"
    ):
        validate_code_postal(code_postal)


@pytest.mark.parametrize("code_postal", [["45A90", "AAAAA"]])
def test_validate_code_postal_fail_2(code_postal: list[str]):
    with pytest.raises(ValueError, match="Au moins un code postal est non valide."):
        validate_code_postal(code_postal)
