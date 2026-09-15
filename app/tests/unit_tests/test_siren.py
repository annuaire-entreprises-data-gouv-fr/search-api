from types import SimpleNamespace

from app.elastic.helpers.helpers import get_doc_id_from_page
from app.elastic.parsers.siren import clean_siren, is_siren


def test_valid_siren():
    assert is_siren("123456789")
    assert is_siren(" 123456789 ")  # Leading/trailing spaces


def test_invalid_siren_length():
    assert not is_siren("12345678")  # Too short
    assert not is_siren("1234567890")  # Too long


def test_invalid_siren_characters():
    assert not is_siren("12345678a")  # Contains a letter
    assert not is_siren("12345678!")  # Contains a special character


def test_none_and_non_string_inputs():
    assert not is_siren(None)
    assert not is_siren(123456789)  # Integer input
    assert not is_siren([])  # List input
    assert not is_siren({})  # Dictionary input


def test_sql_injection():
    assert not is_siren("123456789; DROP TABLE users;")  # SQL injection attempt
    assert not is_siren("' OR '1'='1")  # Common SQL injection pattern


def _builder(terms, page_etablissements):
    return SimpleNamespace(
        search_params=SimpleNamespace(
            terms=terms, page_etablissements=page_etablissements
        )
    )


def test_clean_siren_strips_spaces():
    assert clean_siren("356 000 000") == "356000000"


def test_get_doc_id_strips_spaces():
    assert get_doc_id_from_page(_builder("356 000 000", 1)) == "356000000-100"


def test_get_doc_id_without_spaces():
    assert get_doc_id_from_page(_builder("356000000", 1)) == "356000000-100"
