import pytest

from app.utils.helpers import convert_to_year_month


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("07/04/1970", "1970-04"),  # DD/MM/YYYY
        ("1974-05-18", "1974-05"),  # YYYY-MM-DD
        ("01-01-2022", "2022-01"),  # YYYY-MM-DD
        ("01/2023", None),  # invalid
        ("not-a-date", None),  # invalid
    ],
)
def test_convert_to_year_month(date_string, expected):
    assert convert_to_year_month(date_string) == expected
