from app.elastic.parsers.siren import is_siren


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
