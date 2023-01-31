import pytest
from aio_proxy.labels.helpers import natures_juridiques
from aio_proxy.parsers.nature_juridique import validate_nature_juridique


@pytest.mark.parametrize(
    "nature_juridique, expected",
    [(["1000", "5658"], ["1000", "5658"]), ([], [])],
)
def test_validate_nature_juridique(nature_juridique: str, expected: str):
    assert validate_nature_juridique(nature_juridique) == expected


@pytest.mark.parametrize("nature_juridique", [["123!", "1111, 7344"]])
def test_validate_nature_juridique_fail(
    nature_juridique: str,
):
    with pytest.raises(
        ValueError,
        match=(
            f"Au moins une nature juridique est non valide."
            f"Les natures juridiques valides"
            f" : {[nature_juridique for nature_juridique in natures_juridiques]}"
        ),
    ):
        validate_nature_juridique(nature_juridique)
