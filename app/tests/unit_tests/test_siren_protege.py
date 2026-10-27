import logging

import pytest
import requests

from app.service import siren_protege
from app.service.siren_protege import (
    SirenProtegeList,
    is_siren_protege,
    parse_siren_protege_csv,
    siren_protege_list,
)


class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


@pytest.fixture(autouse=True)
def empty_siren_protege_list():
    siren_protege_list.set_sirens(frozenset())
    yield
    siren_protege_list.set_sirens(frozenset())


def build_list_returning(monkeypatch, response, sirens_flagged_in_index=frozenset()):
    def fake_get(url, timeout):
        if isinstance(response, Exception):
            raise response
        return response

    def fake_find_sirens_indexed_as_protege(sirens):
        if isinstance(sirens_flagged_in_index, Exception):
            raise sirens_flagged_in_index
        return sirens_flagged_in_index & sirens

    monkeypatch.setattr(siren_protege.requests, "get", fake_get)
    monkeypatch.setattr(
        siren_protege,
        "find_sirens_indexed_as_protege",
        fake_find_sirens_indexed_as_protege,
    )
    return SirenProtegeList(url="https://example.com/s.csv", refresh_interval_seconds=1)


def test_parse_siren_protege_csv_returns_sirens():
    assert parse_siren_protege_csv("siren\n123456789\n987654321\n") == {
        "123456789",
        "987654321",
    }


def test_parse_siren_protege_csv_with_header_only_returns_empty_set():
    assert parse_siren_protege_csv("siren\n") == frozenset()


def test_parse_siren_protege_csv_ignores_invalid_sirens():
    assert parse_siren_protege_csv("siren\n123456789\n12345\n\n") == {"123456789"}


@pytest.mark.parametrize("content", ["", "siret\n12345678900011\n"])
def test_parse_siren_protege_csv_without_siren_column_raises(content):
    with pytest.raises(ValueError):
        parse_siren_protege_csv(content)


def test_refresh_replaces_list(monkeypatch):
    protected = build_list_returning(monkeypatch, FakeResponse("siren\n123456789\n"))
    protected.set_sirens(frozenset({"987654321"}))

    assert protected.refresh() is True
    assert "123456789" in protected
    assert "987654321" not in protected


def test_refresh_with_empty_csv_empties_list(monkeypatch):
    protected = build_list_returning(monkeypatch, FakeResponse("siren\n"))
    protected.set_sirens(frozenset({"987654321"}))

    assert protected.refresh() is True
    assert protected.sirens_not_flagged_in_index == ()


@pytest.mark.parametrize(
    "response",
    [
        FakeResponse("", status_code=503),
        FakeResponse("<html>Not found</html>"),
        requests.ConnectionError("unreachable"),
    ],
)
def test_failed_refresh_keeps_last_known_list(monkeypatch, response):
    protected = build_list_returning(monkeypatch, response)
    protected.set_sirens(frozenset({"987654321"}))

    assert protected.refresh() is False
    assert "987654321" in protected


def test_refresh_keeps_only_sirens_not_flagged_in_index_for_queries(monkeypatch):
    protected = build_list_returning(
        monkeypatch,
        FakeResponse("siren\n123456789\n987654321\n"),
        sirens_flagged_in_index=frozenset({"123456789"}),
    )

    assert protected.refresh() is True
    assert protected.sirens_not_flagged_in_index == ("987654321",)
    assert "123456789" in protected


def test_refresh_keeps_all_sirens_for_queries_when_index_check_fails(monkeypatch):
    protected = build_list_returning(
        monkeypatch,
        FakeResponse("siren\n123456789\n987654321\n"),
        sirens_flagged_in_index=ConnectionError("elasticsearch unreachable"),
    )

    assert protected.refresh() is True
    assert protected.sirens_not_flagged_in_index == ("123456789", "987654321")


def test_sirens_not_flagged_in_index_are_sorted():
    protected = SirenProtegeList(url="https://example.com", refresh_interval_seconds=1)
    protected.set_sirens(frozenset({"300000000", "100000000", "200000000"}))

    assert protected.sirens_not_flagged_in_index == (
        "100000000",
        "200000000",
        "300000000",
    )


def test_is_siren_protege_when_indexed_as_protected():
    assert is_siren_protege({"siren": "123456789", "est_protege": True}) is True


def test_is_siren_protege_when_in_memory_list():
    siren_protege_list.set_sirens(frozenset({"123456789"}))

    assert is_siren_protege({"siren": "123456789", "est_protege": False}) is True


def test_is_not_siren_protege_when_absent_from_index_and_list():
    assert is_siren_protege({"siren": "123456789"}) is False


def test_first_refresh_logs_list_even_if_empty(monkeypatch, caplog):
    protected = build_list_returning(monkeypatch, FakeResponse("siren\n"))

    with caplog.at_level(logging.INFO, logger=siren_protege.__name__):
        protected.refresh()

    assert "0 SIREN (+0 / -0)" in caplog.text


def test_refresh_logs_added_and_removed_sirens(monkeypatch, caplog):
    protected = build_list_returning(
        monkeypatch, FakeResponse("siren\n123456789\n111111111\n")
    )
    protected.set_sirens(frozenset({"987654321"}))
    protected._has_loaded = True

    with caplog.at_level(logging.INFO, logger=siren_protege.__name__):
        protected.refresh()

    assert "2 SIREN (+2 / -1)" in caplog.text


def test_refresh_does_not_log_when_nothing_changed(monkeypatch, caplog):
    protected = build_list_returning(monkeypatch, FakeResponse("siren\n123456789\n"))
    protected.refresh()

    with caplog.at_level(logging.INFO, logger=siren_protege.__name__):
        protected.refresh()

    assert caplog.text == ""


def test_refresh_logs_when_sirens_get_flagged_in_index(monkeypatch, caplog):
    protected = build_list_returning(
        monkeypatch,
        FakeResponse("siren\n123456789\n"),
        sirens_flagged_in_index=frozenset({"123456789"}),
    )
    protected.set_sirens(frozenset({"123456789"}))
    protected._has_loaded = True

    with caplog.at_level(logging.INFO, logger=siren_protege.__name__):
        protected.refresh()

    assert "(+0 / -0), 0 not yet flagged in the index" in caplog.text
