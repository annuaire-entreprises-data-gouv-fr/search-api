import pytest
from aio_proxy.parsers.section_activite_principale import (
    validate_section_activite_principale,
)


@pytest.mark.parametrize(
    "section_activite_principale, expected",
    [(["A", "A"]), ([], [])],
)
def test_validate_section_activite_principale(
    section_activite_principale: str, expected: str
):
    assert validate_section_activite_principale(section_activite_principale) == expected


@pytest.mark.parametrize("section_activite_principale", [["Z", "68.20B"]])
def test_validate_section_activite_principale_fail(
    section_activite_principale: str,
):
    with pytest.raises(
        ValueError,
        match="Au moins une section d'activité principale est non valide.",
    ):
        validate_section_activite_principale(section_activite_principale)
