import pytest
from aio_proxy.utils.helpers import convert_to_year_month


@pytest.mark.parametrize(
    "date_string, expected",
    [("07/04/1970", "1970-04"), ("01-01-2022", None), ("01/2023", None)],
)
def test_convert_to_year_month(date_string, expected):
    assert convert_to_year_month(date_string) == expected
