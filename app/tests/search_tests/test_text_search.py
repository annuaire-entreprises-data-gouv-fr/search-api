"""Recherche textuelle (`/search?q=…`) : chaque champ indexé doit être cherché.

Le `text_query` construit par `app/elastic/queries/text.py` interroge une
dizaine de champs différents, certains au niveau de l'unité légale, d'autres
dans les établissements imbriqués. Un champ retiré par erreur de cette liste ne
casse aucun test unitaire : il rend juste une entité introuvable. Ces tests
couvrent donc un chemin de recherche par champ.
"""

from app.tests.search_tests.search_fixtures import (
    ARCTURUS,
    CNRS,
    COMMUNE_DE_LAMBESC,
    DIRIGEANT_NOM,
    DIRIGEANT_PRENOM_EXACT,
    EDF,
    ELU_NOM,
    GANYMEDE,
    GANYMEDE_LAMBESC,
    GANYMEDE_NARBONNE,
    GANYMEDE_NOM_COMMERCIAL,
    LA_POSTE,
    LA_POSTE_ANCIEN_SIREN,
    LA_POSTE_SABLE_ADRESSE,
    LA_POSTE_SABLE_CODE_POSTAL,
    LA_POSTE_SABLE_SIRET,
    MASQUE_NON_DIFFUSIBLE,
    NOM_COMMERCIAL_FRIANDISES,
    NON_DIFFUSIBLE_PERSONNE_PHYSIQUE,
    OGF_ADRESSE_DROUOT,
    OGF_ENSEIGNE,
    OGF_SERVICES_FUNERAIRES,
    PERSONNE_PHYSIQUE_ALLIETTA,
    PERSONNE_PHYSIQUE_ALLIETTA_NOM_COMPLET,
    RNA_SECOURS_POPULAIRE,
    SECOURS_POPULAIRE_RNA,
    TERMES_INEXISTANTS,
)


def test_search_by_nom_complet(api_response_tester):
    api_response_tester.assert_first_siren("search?q=la poste", LA_POSTE)


def test_search_by_nom_raison_sociale(api_response_tester):
    api_response_tester.assert_first_siren("search?q=electricite de france", EDF)


def test_search_by_sigle(api_response_tester):
    api_response_tester.assert_first_siren("search?q=cnrs", CNRS)
    api_response_tester.assert_siren_in_results("search?q=edf", EDF, 5)


def test_search_by_denomination_cross_fields(api_response_tester):
    api_response_tester.assert_first_siren("search?q=electricite de france edf", EDF)


def test_search_by_nom_et_prenom_personne_physique(api_response_tester):
    path = f"search?q={PERSONNE_PHYSIQUE_ALLIETTA_NOM_COMPLET}"
    api_response_tester.assert_first_siren(path, PERSONNE_PHYSIQUE_ALLIETTA)
    # Sans le trait d'union, l'entité reste trouvable (analyse du texte).
    api_response_tester.assert_first_siren(
        "search?q=jean louis allietta", PERSONNE_PHYSIQUE_ALLIETTA
    )


def test_search_by_identifiant_association(api_response_tester):
    path = f"search?q={RNA_SECOURS_POPULAIRE}"
    api_response_tester.assert_first_siren(path, SECOURS_POPULAIRE_RNA)
    assert api_response_tester.get_total_results(path) == 1


def test_search_by_identifiant_association_is_case_insensitive(
    api_response_tester,
):
    path = f"search?q={RNA_SECOURS_POPULAIRE.lower()}"
    api_response_tester.assert_first_siren(path, SECOURS_POPULAIRE_RNA)


def test_search_by_enseigne(api_response_tester):
    api_response_tester.assert_siren_in_results(
        f"search?q={OGF_ENSEIGNE}", OGF_SERVICES_FUNERAIRES, 5
    )


def test_search_by_nom_commercial(api_response_tester):
    api_response_tester.assert_siren_in_results(
        f"search?q={NOM_COMMERCIAL_FRIANDISES}", GANYMEDE_NOM_COMMERCIAL
    )


def test_search_by_adresse(api_response_tester):
    api_response_tester.assert_first_siren(
        f"search?q={LA_POSTE_SABLE_ADRESSE}", LA_POSTE
    )


def test_search_by_commune(api_response_tester):
    api_response_tester.assert_first_siren(
        "search?q=ganymede lambesc", GANYMEDE_LAMBESC
    )
    api_response_tester.assert_first_siren(
        "search?q=ganymede narbonne", GANYMEDE_NARBONNE
    )
    api_response_tester.assert_siren_not_in_results(
        "search?q=ganymede narbonne", GANYMEDE_LAMBESC
    )


def test_matching_etablissements_are_limited_by_parameter(api_response_tester):
    for limit in (1, 3, 25):
        results = api_response_tester.get_results(
            f"search?q=la poste&limite_matching_etablissements={limit}"
        )
        assert len(results[0]["matching_etablissements"]) == limit


def test_search_by_nom_dirigeant(api_response_tester):
    path = f"search?q={DIRIGEANT_NOM} {DIRIGEANT_PRENOM_EXACT}"
    sirens = api_response_tester.get_sirens(path)
    assert ARCTURUS in sirens
    assert GANYMEDE in sirens


def test_search_by_nom_elu(api_response_tester):
    api_response_tester.assert_siren_in_results(
        f"search?q={ELU_NOM} helene", COMMUNE_DE_LAMBESC
    )


def test_search_by_siren_accepts_spaces(api_response_tester):
    api_response_tester.assert_first_siren("search?q=356 000 000", LA_POSTE)


def test_search_by_siret_accepts_spaces(api_response_tester):
    path = "search?q=356 000 000 24221"
    api_response_tester.assert_first_siren(path, LA_POSTE)
    results = api_response_tester.get_results(path)
    assert results[0]["matching_etablissements"][0]["siret"] == LA_POSTE_SABLE_SIRET


def test_siren_search_ignores_other_filters(api_response_tester):
    for extra_filter in ("code_postal=13000", "est_bio=true", "departement=13"):
        path = f"search?q={LA_POSTE}&{extra_filter}"
        api_response_tester.assert_first_siren(path, LA_POSTE)
        assert api_response_tester.get_total_results(path) == 1


def test_search_by_number_that_is_neither_siren_nor_siret(api_response_tester):
    path = f"search?q={LA_POSTE}1"
    assert api_response_tester.get_total_results(path) == 0


def test_page_etablissements_returns_distinct_etablissements(
    api_response_tester,
):
    """Au-delà de 100 entreprises, le payload est paginé par sous-document."""
    path = f"search?q={LA_POSTE}&include_admin=etablissements&page_etablissements="
    first_page = api_response_tester.get_results(f"{path}1")[0]["etablissements"]
    second_page = api_response_tester.get_results(f"{path}2")[0]["etablissements"]

    assert len(first_page) == 100
    assert len(second_page) == 100
    first_sirets = {etablissement["siret"] for etablissement in first_page}
    second_sirets = {etablissement["siret"] for etablissement in second_page}
    assert not first_sirets & second_sirets


def test_text_search_is_case_insensitive(api_response_tester):
    lowercase = api_response_tester.get_json("search?q=electricite de france")
    uppercase = api_response_tester.get_json("search?q=ELECTRICITE DE FRANCE")
    assert lowercase["total_results"] == uppercase["total_results"]
    assert [result["siren"] for result in lowercase["results"]] == [
        result["siren"] for result in uppercase["results"]
    ]


def test_text_search_is_accent_insensitive(api_response_tester):
    without_accents = api_response_tester.get_json("search?q=electricite de france")
    with_accents = api_response_tester.get_json("search?q=électricité de france")
    assert without_accents["total_results"] == with_accents["total_results"]
    assert with_accents["results"][0]["siren"] == EDF


def test_text_search_requires_all_terms(api_response_tester):
    """Toutes les clauses textuelles utilisent `operator: AND`."""
    assert api_response_tester.get_total_results("search?q=la poste zzzqqqwww") == 0


def test_search_unknown_terms_returns_empty_response(api_response_tester):
    path = f"search?q={TERMES_INEXISTANTS}"
    response = api_response_tester.get_json(path)
    assert response["total_results"] == 0
    assert response["results"] == []


def test_search_enseigne_and_adresse(api_response_tester):
    path = f"search?q={OGF_ENSEIGNE} {OGF_ADRESSE_DROUOT}"
    api_response_tester.assert_first_siren(path, OGF_SERVICES_FUNERAIRES)
    etablissement = api_response_tester.get_results(path)[0]["matching_etablissements"][
        0
    ]
    assert "DROUOT" in etablissement["adresse"]


def test_search_denomination_and_commune_narrows_results(api_response_tester):
    total_without_commune = api_response_tester.get_total_results("search?q=la poste")
    total_with_commune = api_response_tester.get_total_results(
        "search?q=la poste lambesc"
    )
    assert total_with_commune < total_without_commune


def test_search_denomination_and_nom_dirigeant_with_person_filters(
    api_response_tester,
):
    path = f"search?q=arcturus&nom_personne={DIRIGEANT_NOM}"
    api_response_tester.assert_first_siren(path, ARCTURUS)
    assert api_response_tester.get_total_results(path) == 1
    api_response_tester.assert_siren_not_in_results(path, GANYMEDE)


def test_search_denomination_and_nom_dirigeant_in_a_single_query(
    api_response_tester,
):
    path = f"search?q=arcturus {DIRIGEANT_NOM}"
    api_response_tester.assert_first_siren(path, ARCTURUS)


def test_text_search_with_matching_etablissement_filter(api_response_tester):
    path = (
        f"search?q=la poste&code_postal={LA_POSTE_SABLE_CODE_POSTAL}"
        "&limite_matching_etablissements=25"
    )
    api_response_tester.assert_first_siren(path, LA_POSTE)
    api_response_tester.assert_siren_ranked_before(
        path, LA_POSTE, LA_POSTE_ANCIEN_SIREN
    )
    for result in api_response_tester.get_results(path):
        assert result["matching_etablissements"]
        for etablissement in result["matching_etablissements"]:
            assert etablissement["code_postal"] == LA_POSTE_SABLE_CODE_POSTAL


def test_text_search_with_unite_legale_etat_filter(api_response_tester):
    for etat in ("A", "C"):
        results = api_response_tester.get_results(
            f"search?q=la poste&etat_administratif={etat}"
        )
        assert results
        for result in results:
            assert result["etat_administratif"] == etat


def test_text_search_with_filter_accepts_short_terms(api_response_tester):
    """Moins de 3 caractères est accepté tant qu'un filtre est présent."""
    api_response_tester.assert_api_response_code_200(
        f"search?q=ab&code_postal={LA_POSTE_SABLE_CODE_POSTAL}"
    )
    api_response_tester.assert_api_response_code_400("search?q=ab")


def test_text_search_never_returns_masked_personne_physique(api_response_tester):
    """Une PP non diffusible ne doit jamais sur une recherche textuelle."""
    for path in ("search?q=martin&per_page=25", "search?q=dupont&per_page=25"):
        for result in api_response_tester.get_results(path):
            assert result["nom_complet"] != MASQUE_NON_DIFFUSIBLE

    api_response_tester.assert_first_siren(
        f"search?q={NON_DIFFUSIBLE_PERSONNE_PHYSIQUE}",
        NON_DIFFUSIBLE_PERSONNE_PHYSIQUE,
    )


def test_page_etablissements_accepts_a_siren_with_spaces(api_response_tester):
    path = "search?q=356 000 000&page_etablissements=1&include_admin=etablissements"
    api_response_tester.assert_first_siren(path, LA_POSTE)
