import pytest
from aio_proxy.parsers.nature_juridique import (
    validate_nature_juridique,
)


@pytest.mark.parametrize(
    "nature_juridique, expected",
    [(["1000", "5658"], ["1000", "5658"]), ([], [])],
)
def test_validate_nature_juridique(nature_juridique: str, expected: str):
    assert validate_nature_juridique(nature_juridique) == expected


@pytest.mark.parametrize("nature_juridique", [["123!", "73, 7344"]])
def test_validate_nature_juridique_fail(
    nature_juridique: str,
):
    with pytest.raises(
        ValueError,
        match="Au moins une nature juridique est non valide.",
    ):
        validate_nature_juridique(nature_juridique)
