import pytest
from aio_proxy.parsers.convention_collective import validate_id_convention_collective
from aio_proxy.parsers.bool_fields import validate_bool_field

@pytest.mark.parametrize(
    "convention_collective_renseignee, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_convention_collective_renseignee(
    convention_collective_renseignee,
    expected,
):
    assert (
        validate_bool_field(
            "convention_collective_renseignee", convention_collective_renseignee
        )
        == expected
    )


@pytest.mark.parametrize(
    "id_convention_collective, expected",
    [("1501", "1501"), ("9432", "9432"), (None, None)],
)
def test_validate_id_convention_collective(id_convention_collective, expected):
    assert validate_id_convention_collective(id_convention_collective) == expected


@pytest.mark.parametrize("id_convention_collective", ["12345", "150"])
def test_validate_id_convention_collective_fail(id_convention_collective: str):
    with pytest.raises(
        ValueError,
        match="L'identifiant de convention collective doit contenir 4 caractères.",
    ):
        validate_id_convention_collective(id_convention_collective)
