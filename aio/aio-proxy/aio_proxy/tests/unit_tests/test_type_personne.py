import pytest
from aio_proxy.parsers.type_personne import validate_type_personne


@pytest.mark.parametrize(
    "type_personne, expected",
    [("ELU", "ELU"), ("DIRIGEANT", "DIRIGEANT"), (None, None)],
)
def test_validate_type_personne(type_personne: str, expected: str):
    assert validate_type_personne(type_personne) == expected


@pytest.mark.parametrize("type_personne", ["DIR", "GERANT"])
def test_validate_type_personne_fail(type_personne: str):
    with pytest.raises(
        ValueError, match="type_personne doit prendre la valeur 'dirigeant' ou 'elu' !"
    ):
        validate_type_personne(type_personne)
