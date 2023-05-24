import pytest
from aio_proxy.request.parsers.collectivite_territoriale import (
    validate_code_collectivite_territoriale,
)


@pytest.mark.parametrize(
    "code_collectivite_territoriale, expected",
    [(["23150", "11"], ["23150", "11"]), ([], [])],
)
def test_validate_code_collectivite_territoriale(
    code_collectivite_territoriale,
    expected,
):
    assert (
        validate_code_collectivite_territoriale(
            code_collectivite_territoriale,
        )
        == expected
    )


@pytest.mark.parametrize("code_collectivite_territoriale", [["1", "2"]])
def test_validate_code_collectivite_territoriale_fail(
    code_collectivite_territoriale: list[str],
):
    with pytest.raises(
        ValueError,
        match="Chaque identifiant code insee d'une collectivité territoriale doit "
        "contenir au moins 2 caractères.",
    ):
        validate_code_collectivite_territoriale(code_collectivite_territoriale)
