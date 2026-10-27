from types import SimpleNamespace

import pytest

from app.service.format_search_results import format_single_unite_legale
from app.service.formatters.non_diffusible import NON_DIFFUSIBLE_MASK
from app.service.siren_protege import siren_protege_list

SEARCH_PARAMS = SimpleNamespace(
    minimal=True,
    include=["SIEGE", "DIRIGEANTS", "MATCHING_ETABLISSEMENTS"],
    include_admin=None,
)

ETABLISSEMENT = {
    "siret": "12345678900011",
    "adresse": "12 RUE DE LA PAIX 75002 PARIS",
    "numero_voie": "12",
    "libelle_voie": "DE LA PAIX",
    "code_postal": "75002",
    "commune": "75102",
    "libelle_commune": "PARIS",
    "latitude": "48.86",
    "longitude": "2.33",
    "nom_commercial": "CHEZ JEAN",
    "statut_diffusion_etablissement": "O",
    "est_siege": True,
}


def build_search_result(**unite_legale):
    return {
        "unite_legale": {
            "siren": "123456789",
            "nom_complet": "JEAN DUPONT",
            "nom_raison_sociale": None,
            "est_personne_morale_insee": False,
            "statut_diffusion_unite_legale": "O",
            "est_protege": False,
            "siege": dict(ETABLISSEMENT),
            "dirigeants_pp": [
                {"nom": "DUPONT", "prenoms": "JEAN", "date_de_naissance": "1980-01"}
            ],
            **unite_legale,
        },
        "matching_etablissements": [dict(ETABLISSEMENT)],
    }


@pytest.fixture(autouse=True)
def empty_siren_protege_list():
    siren_protege_list.set_sirens(frozenset())
    yield
    siren_protege_list.set_sirens(frozenset())


def test_diffusible_unite_legale_is_not_masked():
    result = format_single_unite_legale(build_search_result(), SEARCH_PARAMS)

    assert result["est_protege"] is False
    assert result["nom_complet"] == "JEAN DUPONT (CHEZ JEAN)"
    assert result["siege"]["adresse"] == ETABLISSEMENT["adresse"]
    assert result["dirigeants"][0]["nom"] == "DUPONT"


@pytest.mark.parametrize(
    "in_memory_sirens,est_protege",
    [(frozenset(), True), (frozenset({"123456789"}), False)],
    ids=["indexed_as_protected", "in_memory_list"],
)
def test_protected_unite_legale_is_masked_like_non_diffusible(
    in_memory_sirens, est_protege
):
    siren_protege_list.set_sirens(in_memory_sirens)

    result = format_single_unite_legale(
        build_search_result(est_protege=est_protege), SEARCH_PARAMS
    )

    assert result["est_protege"] is True
    assert result["statut_diffusion"] == "O"
    assert result["nom_complet"] == NON_DIFFUSIBLE_MASK
    for etablissement in (result["siege"], result["matching_etablissements"][0]):
        assert etablissement["adresse"] == NON_DIFFUSIBLE_MASK
        assert etablissement["latitude"] == NON_DIFFUSIBLE_MASK
        assert etablissement["nom_commercial"] == NON_DIFFUSIBLE_MASK
        assert etablissement["libelle_commune"] == "PARIS"
    assert result["dirigeants"][0]["nom"] == NON_DIFFUSIBLE_MASK
    assert result["dirigeants"][0]["prenoms"] == NON_DIFFUSIBLE_MASK


def test_protected_personne_morale_keeps_raison_sociale():
    siren_protege_list.set_sirens(frozenset({"123456789"}))

    result = format_single_unite_legale(
        build_search_result(
            nom_complet="SOCIETE DUPONT",
            nom_raison_sociale="SOCIETE DUPONT",
            sigle="SD",
            est_personne_morale_insee=True,
        ),
        SEARCH_PARAMS,
    )

    assert result["est_protege"] is True
    assert result["nom_raison_sociale"] == "SOCIETE DUPONT"
    assert result["sigle"] == NON_DIFFUSIBLE_MASK
    assert result["siege"]["adresse"] == NON_DIFFUSIBLE_MASK
