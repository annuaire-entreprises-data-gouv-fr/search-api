from app.elastic.parsers.numero_rnf import is_numero_rnf


def test_valid_numero_rnf():
    assert is_numero_rnf("092-FDD-00061-08")
    assert is_numero_rnf("075-FE-00129-09")
    assert is_numero_rnf("092-FRUP-00062-08")
    assert is_numero_rnf(" 073-FDD-00072-04 ")
    assert is_numero_rnf("073-fdd-00072-04")


def test_invalid_numero_rnf_shape():
    assert not is_numero_rnf("073FDD0007204")
    assert not is_numero_rnf("73-FDD-00072-04")
    assert not is_numero_rnf("073-FDD-0072-04")
    assert not is_numero_rnf("073-FDD-00072")
    assert not is_numero_rnf("073-FONDATION-00072-04")
    assert not is_numero_rnf("073-123-00072-04")
    assert not is_numero_rnf("073-FDD-00072-04-01")


def test_none_and_non_string_inputs():
    assert not is_numero_rnf(None)
    assert not is_numero_rnf(73)
    assert not is_numero_rnf([])
    assert not is_numero_rnf({})


def test_injection():
    assert not is_numero_rnf("073-FDD-00072-04 OR 1=1")
    assert not is_numero_rnf("*")
