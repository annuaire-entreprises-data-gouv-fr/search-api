import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field
from aio_proxy.parsers.collectivite_territoriale import (
    validate_code_collectivite_territoriale,
)


@pytest.mark.parametrize(
    "est_collectivite_territoriale, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_est_collectivite_territoriale(
    est_collectivite_territoriale,
    expected,
):
    assert (
        validate_bool_field(
            "est_collectivite_territoriale", est_collectivite_territoriale
        )
        == expected
    )


@pytest.mark.parametrize(
    "est_collectivite_territoriale",
    ["NON", "OUI", "NO", "YES"],
)
def test_validate_est_collectivite_territoriale_fail(
    est_collectivite_territoriale: str,
):
    with pytest.raises(
        ValueError,
        match="est_collectivite_territoriale doit prendre la valeur 'true' "
        "ou 'false' !",
    ):
        validate_bool_field(
            "est_collectivite_territoriale",
            est_collectivite_territoriale,
        )


@pytest.mark.parametrize(
    "code_collectivite_territoriale, expected",
    [("23150", "23150"), ("11", "11"), (None, None)],
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


@pytest.mark.parametrize("code_collectivite_territoriale", ["1", "2"])
def test_validate_code_collectivite_territoriale_fail(
    code_collectivite_territoriale: str,
):
    with pytest.raises(
        ValueError,
        match="L'identifiant code_insee d'une collectivité "
        "territoriale doit contenir au moins 2 caractères.",
    ):
        validate_code_collectivite_territoriale(code_collectivite_territoriale)
