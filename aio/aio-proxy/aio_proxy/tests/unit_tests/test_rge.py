import pytest
from aio_proxy.parsers.exist_fields import validate_est_field
from aio_proxy.parsers.rge import validate_id_rge


@pytest.mark.parametrize(
    "est_rge, expected",
    [("TRUE", True), ("FALSE", False), (None, None)],
)
def test_validate_est_rge(est_rge, expected):
    assert validate_est_field("est_rge", est_rge) == expected

@pytest.mark.parametrize("est_rge", ["NON", "OUI", "NO", "YES"])
def test_validate_est_rge_fail(
    est_rge: str,
):
    with pytest.raises(
        ValueError,
        match="est_rge doit prendre la valeur 'true' "
        "or 'false' !",
    ):
        validate_est_field("est_rge", est_rge)

@pytest.mark.parametrize(
    "id_rge, expected",
    [("8621T18D109", "8621T18D109"), ("1", "1"), (None, None)],
)
def test_validate_id_rge(id_rge, expected):
    assert validate_id_rge(id_rge) == expected
