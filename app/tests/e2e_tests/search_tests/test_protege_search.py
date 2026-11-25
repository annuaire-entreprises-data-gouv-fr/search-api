"""SIREN protégés historiques (site#2837).

Adresse masquée sauf la commune, identité des dirigeants masquée. Pour une unité
légale qui n'est pas une PM (EI, nature juridique 2xxx), la commune et la dénomination
sont aussi masquées et seul le SIREN permet de la trouver.
"""

import pytest

from app.tests.e2e_tests.search_tests.search_fixtures import (
    MASQUE_PROTEGE,
    PROTEGE_LEGACY_EI,
    PROTEGE_LEGACY_NON_PM,
    PROTEGE_LEGACY_NON_PM_FILTRES,
    PROTEGE_LEGACY_PM,
    PROTEGE_LEGACY_PM_CODE_COMMUNE,
    PROTEGE_LEGACY_PM_NOM,
)

PROTEGE_LEGACY = (PROTEGE_LEGACY_PM, PROTEGE_LEGACY_EI, PROTEGE_LEGACY_NON_PM)
PROTEGE_LEGACY_NON_PMS = (PROTEGE_LEGACY_EI, PROTEGE_LEGACY_NON_PM)
ADRESSE_FIELDS = ("adresse", "code_postal", "libelle_voie", "latitude", "longitude")
COMMUNE_FIELDS = ("commune", "libelle_commune", "epci")
DENOMINATION_FIELDS = ("nom_complet", "nom_raison_sociale", "sigle")
DIRIGEANT_PP_FIELDS = (
    "nom",
    "prenoms",
    "nationalite",
    "annee_de_naissance",
    "date_de_naissance",
)


def get_unite_legale(api_response_tester, siren):
    return api_response_tester.get_results(f"search?q={siren}")[0]


@pytest.mark.parametrize("siren", PROTEGE_LEGACY)
def test_protege_legacy_found_by_siren(api_response_tester, siren):
    api_response_tester.assert_first_siren(f"search?q={siren}", siren)


@pytest.mark.parametrize("siren", PROTEGE_LEGACY)
def test_protege_legacy_masks_adresse(api_response_tester, siren):
    siege = get_unite_legale(api_response_tester, siren)["siege"]
    for field in ADRESSE_FIELDS:
        assert siege[field] == MASQUE_PROTEGE, field


def test_protege_legacy_pm_keeps_commune(api_response_tester):
    siege = get_unite_legale(api_response_tester, PROTEGE_LEGACY_PM)["siege"]
    for field in COMMUNE_FIELDS:
        assert siege[field] not in (None, MASQUE_PROTEGE), field


@pytest.mark.parametrize("siren", PROTEGE_LEGACY_NON_PMS)
def test_protege_legacy_non_pm_masks_commune(api_response_tester, siren):
    siege = get_unite_legale(api_response_tester, siren)["siege"]
    for field in COMMUNE_FIELDS:
        assert siege[field] == MASQUE_PROTEGE, field


@pytest.mark.parametrize("siren", (PROTEGE_LEGACY_PM, PROTEGE_LEGACY_EI))
def test_protege_legacy_masks_dirigeant_pp_identity(api_response_tester, siren):
    dirigeants = get_unite_legale(api_response_tester, siren)["dirigeants"]
    assert dirigeants
    for dirigeant in dirigeants:
        for field in DIRIGEANT_PP_FIELDS:
            assert dirigeant[field] == MASQUE_PROTEGE, field


def test_protege_legacy_keeps_dirigeant_qualite(api_response_tester):
    dirigeant = get_unite_legale(api_response_tester, PROTEGE_LEGACY_PM)["dirigeants"][
        0
    ]
    assert dirigeant["qualite"] not in (None, MASQUE_PROTEGE)


def test_protege_legacy_pm_keeps_denomination(api_response_tester):
    unite_legale = get_unite_legale(api_response_tester, PROTEGE_LEGACY_PM)
    assert unite_legale["nom_complet"] == PROTEGE_LEGACY_PM_NOM.upper()


@pytest.mark.parametrize("siren", PROTEGE_LEGACY_NON_PMS)
def test_protege_legacy_non_pm_masks_denomination_even_when_empty(
    api_response_tester, siren
):
    unite_legale = get_unite_legale(api_response_tester, siren)
    for field in DENOMINATION_FIELDS:
        assert unite_legale[field] == MASQUE_PROTEGE, field
    assert unite_legale["siege"]["nom_commercial"] == MASQUE_PROTEGE
    assert unite_legale["siege"]["liste_enseignes"] == [MASQUE_PROTEGE]


def test_protege_legacy_non_pm_excluded_from_filter_search(api_response_tester):
    path = f"search?{PROTEGE_LEGACY_NON_PM_FILTRES}&per_page=25"
    assert api_response_tester.get_results(path)
    api_response_tester.assert_siren_not_in_results(path, PROTEGE_LEGACY_NON_PM)


def test_protege_legacy_pm_found_by_nom(api_response_tester):
    api_response_tester.assert_siren_in_results(
        f"search?q={PROTEGE_LEGACY_PM_NOM}", PROTEGE_LEGACY_PM
    )


def test_protege_legacy_pm_found_by_nom_and_code_commune(api_response_tester):
    api_response_tester.assert_siren_in_results(
        f"search?q={PROTEGE_LEGACY_PM_NOM} {PROTEGE_LEGACY_PM_CODE_COMMUNE}",
        PROTEGE_LEGACY_PM,
    )


def test_protege_legacy_pm_kept_when_filtering_on_commune(api_response_tester):
    api_response_tester.assert_siren_in_results(
        f"search?q={PROTEGE_LEGACY_PM_NOM}&commune={PROTEGE_LEGACY_PM_CODE_COMMUNE}",
        PROTEGE_LEGACY_PM,
    )
