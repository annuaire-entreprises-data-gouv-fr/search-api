from app.service.formatters.fondation import format_fondation

FONDATION_WITH_SIRET = {
    "numero_rnf": "092-FDD-00061-08",
    "titre": "FONDS DE DOTATION PRO BONO LAB",
    "type_organisme": "FDD",
    "date_creation": "2015-02-04",
    "siren": "812333425",
    "siret": "81233342500013",
    "adresse": "132 Rue Martre",
    "code_postal": "92110",
    "ville": "Clichy",
}

FONDATION_WITHOUT_SIRET = {
    "numero_rnf": "073-FDD-00072-04",
    "titre": "FONDS DE DOTATION SAVOIE MONT-BLANC BIODIVERSITÉ",
    "type_organisme": "FDD",
    "date_creation": "2023-03-21",
    "adresse": "165 Route de chambéry",
    "code_postal": "73370",
    "ville": "Le Bourget-du-Lac",
}


def test_format_fondation_attached_to_an_unite_legale():
    assert format_fondation(FONDATION_WITH_SIRET) == {
        "numero_rnf": "092-FDD-00061-08",
        "titre": "FONDS DE DOTATION PRO BONO LAB",
        "type_organisme": "FDD",
        "date_creation": "2015-02-04",
        "adresse": "132 Rue Martre",
        "code_postal": "92110",
        "ville": "Clichy",
        "siren": "812333425",
        "siret": "81233342500013",
    }


def test_format_fondation_without_siret():
    """Fondations the RNF does not link to an établissement have no siren/siret."""
    formatted = format_fondation(FONDATION_WITHOUT_SIRET)
    assert formatted["numero_rnf"] == "073-FDD-00072-04"
    assert formatted["siren"] is None
    assert formatted["siret"] is None


def test_format_fondation_converts_date_creation_to_iso():
    fondation = FONDATION_WITH_SIRET | {"date_creation": "2015-02-04T00:00:00"}
    assert format_fondation(fondation)["date_creation"] == "2015-02-04"


def test_format_fondation_without_score_when_no_meta():
    assert "score" not in format_fondation(FONDATION_WITH_SIRET)
