from datetime import date

import pytest

from app.controller.search_params_model import SearchParams
from app.exceptions.exceptions import InvalidParamError
from app.service.search_type import SearchType


def _build_params(**kwargs):
    return SearchParams(search_type=SearchType.TEXT, nom_personne="dupont", **kwargs)


def test_accepts_year_month_min_as_first_day_of_month():
    params = _build_params(min_date_naiss_personne="1990-08")
    assert params.min_date_naiss_personne == date(1990, 8, 1)


def test_accepts_year_month_max_as_last_day_of_month():
    params = _build_params(max_date_naiss_personne="1990-02")
    assert params.max_date_naiss_personne == date(1990, 2, 28)


def test_accepts_year_month_max_on_leap_year():
    params = _build_params(max_date_naiss_personne="2020-02")
    assert params.max_date_naiss_personne == date(2020, 2, 29)


def test_full_date_min_ignores_day_and_keeps_first_day_of_month():
    params = _build_params(min_date_naiss_personne="1990-08-15")
    assert params.min_date_naiss_personne == date(1990, 8, 1)


def test_full_date_max_ignores_day_and_keeps_last_day_of_month():
    params = _build_params(max_date_naiss_personne="1990-08-02")
    assert params.max_date_naiss_personne == date(1990, 8, 31)


def test_rejects_invalid_date_format():
    with pytest.raises(InvalidParamError):
        _build_params(min_date_naiss_personne="13/09/2001")


def test_rejects_invalid_month():
    with pytest.raises(InvalidParamError):
        _build_params(min_date_naiss_personne="1990-13")
