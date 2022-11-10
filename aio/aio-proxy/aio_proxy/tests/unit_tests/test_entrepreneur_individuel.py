import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field


@pytest.mark.parametrize(
    "est_entrepreneur_individuel, expected",
    [("TRUE", True), ("False", False), (None, None)],
)
def test_validate_est_entrepreneur_individuel(est_entrepreneur_individuel, expected):
    assert (
        validate_bool_field("est_entrepreneur_individuel", est_entrepreneur_individuel)
        == expected
    )


@pytest.mark.parametrize("est_entrepreneur_individuel", ["NON", "OUI", "NO", "YES"])
def test_validate_est_entrepreneur_individuel_fail(
    est_entrepreneur_individuel: str,
):
    with pytest.raises(
        ValueError,
        match="est_entrepreneur_individuel doit prendre la valeur 'true' "
        "or 'false' !",
    ):
        validate_bool_field("est_entrepreneur_individuel", est_entrepreneur_individuel)
