import pytest
from aio_proxy.parsers.bool_fields import validate_bool_field


@pytest.mark.parametrize(
    "est_association, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_est_association(est_association, expected):
    assert validate_bool_field("est_association", est_association) == expected


@pytest.mark.parametrize("est_association", ["NON", "OUI", "NO", "YES"])
def test_validate_est_association_fail(
    est_association: str,
):
    with pytest.raises(
        ValueError,
        match="est_association doit prendre la valeur 'true' or 'false' !",
    ):
        validate_bool_field("est_association", est_association)
