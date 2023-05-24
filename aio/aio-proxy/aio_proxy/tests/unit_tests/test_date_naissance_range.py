import pytest
from aio_proxy.request.helpers import validate_date_range


@pytest.mark.parametrize(
    "min_date_naissance, max_date_naissance",
    [("1964-05-08", "1963-06-04")],
)
def test_validate_dates_fail(min_date_naissance: str, max_date_naissance: str):
    with pytest.raises(
        ValueError,
        match="Veuillez indiquer une date minimale inférieure à la date maximale.",
    ):
        validate_date_range(min_date_naissance, max_date_naissance)
