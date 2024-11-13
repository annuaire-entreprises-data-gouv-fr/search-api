from app.elastic.parsers.siret import is_siret


def test_valid_siret():
    assert is_siret("12345678901234")  # Valid SIRET number
    assert is_siret(" 12345678901234 ")  # Valid SIRET number with spaces


def test_invalid_siret_length():
    assert not is_siret("1234567890123")  # Too short
    assert not is_siret("123456789012345")  # Too long


def test_invalid_siret_characters():
    assert not is_siret("1234567890123a")  # Contains a letter
    assert not is_siret("1234567890123!")  # Contains a special character


def test_none_and_non_string_inputs():
    assert not is_siret(None)
    assert not is_siret(12345678901234)
    assert not is_siret([])
    assert not is_siret({})


def test_siret_with_spaces():
    assert is_siret("1234 5678 9012 34")  # Valid SIRET number with spaces
    assert not is_siret("1234 5678 9012 3a")  # Invalid due to letter
