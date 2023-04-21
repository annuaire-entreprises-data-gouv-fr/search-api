import pytest
from aio_proxy.parsers.categorie_entreprise import validate_categorie_entreprise


@pytest.mark.parametrize(
    "categorie_entreprise, expected",
    [(["PME", "GE"], ["PME", "GE"]), ([], [])],
)
def test_validate_categorie_entreprise(categorie_entreprise, expected):
    assert validate_categorie_entreprise(categorie_entreprise) == expected


@pytest.mark.parametrize("categorie_entreprise", [["TRT", "GO"]])
def test_validate_categorie_entreprise_fail(categorie_entreprise: list[str]):
    with pytest.raises(
        ValueError,
        match="Chaque catégorie d'entreprise doit prendre une de ces "
        "valeurs 'GE', 'PME' ou 'ETI'.",
    ):
        validate_categorie_entreprise(categorie_entreprise)
