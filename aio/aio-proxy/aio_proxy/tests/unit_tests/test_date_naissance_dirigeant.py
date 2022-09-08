import pytest
from aio_proxy.parsers.date_parser import parse_date, validate_dates


@pytest.mark.parametrize(
    "min_date_naissance, max_date_naissance",
    [("1964-05-08", "1963-06-04")],
)
def test_validate_dates_fail(min_date: str, max_date: str):
    with pytest.raises(
        ValueError,
        match="Veuillez indiquer une date minimale inférieure à la date maximale.",
    ):
        validate_dates(min_date, max_date)


@pytest.mark.parametrize("date, expected", [("1940-05-06", "1940-05-06")])
def test_parse_date(date: str):
    assert parse_date(date) == expected


@pytest.mark.parametrize("date", ["07/06/1992"])
def test_parse_date_fail(date: str):
    with pytest.raises(
        ValueError,
        match="Veuillez indiquer une date sous le format : aaaa-mm-jj. Exemple : "
        "'1990-01-02'",
    ):
        parse_date(date)
