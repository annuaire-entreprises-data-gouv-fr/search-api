import pytest
from aio_proxy.parsers.nature_juridique import validate_nature_juridique


@pytest.mark.parametrize(
    "nature_juridique, expected",
    [(["1000", "5658"], ["1000", "5658"]), ([], [])],
)
def test_validate_nature_juridique(nature_juridique: list[str], expected: list[str]):
    assert validate_nature_juridique(nature_juridique) == expected


@pytest.mark.parametrize("nature_juridique", [["123!", "11, 7344"]])
def test_validate_nature_juridique_fail(
    nature_juridique,
):
    with pytest.raises(ValueError):
        validate_nature_juridique(nature_juridique)
