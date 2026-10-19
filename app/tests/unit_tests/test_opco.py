from app.models.unite_legale import Opco
from app.service.formatters.opco import format_opco


def test_format_opco_returns_none_without_opco():
    assert format_opco(None, None) is None


def test_format_opco_without_opco_gestion():
    assert format_opco("OPCO EP", None) == Opco(nom="OPCO EP", nom_gestion=None)


def test_format_opco_with_opco_gestion():
    assert format_opco("OPCO EP", "AKTO") == Opco(nom="OPCO EP", nom_gestion="AKTO")
