from app.tests.search_tests.search_fixtures import (
    ARCTURUS,
    COMMUNE_DE_LAMBESC,
    DIRIGEANT_ANNEE_NAISSANCE,
    DIRIGEANT_NOM,
    DIRIGEANT_PRENOM_EXACT,
    DIRIGEANT_PRENOMS_PARTIELS,
    ELU_NOM,
    GANYMEDE,
    MASQUE_NON_DIFFUSIBLE,
)

NOM_PATH = f"search?nom_personne={DIRIGEANT_NOM}"


def test_person_search_by_nom(api_response_tester):
    sirens = api_response_tester.get_sirens(f"{NOM_PATH}&per_page=25")
    assert ARCTURUS in sirens
    assert GANYMEDE in sirens


def test_person_search_by_nom_and_prenoms_narrows_results(api_response_tester):
    total_nom_only = api_response_tester.get_total_results(NOM_PATH)
    total_with_prenom = api_response_tester.get_total_results(
        f"{NOM_PATH}&prenoms_personne={DIRIGEANT_PRENOM_EXACT}"
    )
    assert 0 < total_with_prenom < total_nom_only


def test_person_search_requires_every_prenom(api_response_tester):
    path = f"{NOM_PATH}&prenoms_personne={DIRIGEANT_PRENOMS_PARTIELS}"
    assert api_response_tester.get_sirens(path) == [GANYMEDE]


def test_person_search_is_case_insensitive(api_response_tester):
    lowercase = api_response_tester.get_sirens(f"{NOM_PATH}&per_page=25")
    uppercase = api_response_tester.get_sirens(
        f"search?nom_personne={DIRIGEANT_NOM.upper()}&per_page=25"
    )
    assert lowercase == uppercase


def test_person_search_ignores_particules(api_response_tester):
    without_particles = api_response_tester.get_sirens(f"{NOM_PATH}&per_page=25")
    with_particles = api_response_tester.get_sirens(
        f"search?nom_personne=de la {DIRIGEANT_NOM}&per_page=25"
    )
    assert set(with_particles) == set(without_particles)


def test_person_search_treats_hyphen_as_space(api_response_tester):
    hyphenated = api_response_tester.get_sirens(
        f"{NOM_PATH}&prenoms_personne=xavier-erwan"
    )
    spaced = api_response_tester.get_sirens(f"{NOM_PATH}&prenoms_personne=xavier erwan")
    assert hyphenated == spaced == [GANYMEDE]


def test_person_search_date_range_keeps_matching_persons(api_response_tester):
    path = (
        f"{NOM_PATH}&prenoms_personne={DIRIGEANT_PRENOM_EXACT}"
        f"&date_naissance_personne_min={DIRIGEANT_ANNEE_NAISSANCE}-01-01"
        f"&date_naissance_personne_max={DIRIGEANT_ANNEE_NAISSANCE}-12-31"
    )
    sirens = api_response_tester.get_sirens(path)
    assert ARCTURUS in sirens
    assert GANYMEDE in sirens


def test_person_search_date_range_excludes_other_persons(api_response_tester):
    path = (
        f"{NOM_PATH}&prenoms_personne={DIRIGEANT_PRENOM_EXACT}"
        "&date_naissance_personne_min=1995-01-01"
    )
    assert api_response_tester.get_total_results(path) == 0


def test_person_search_rejects_inverted_date_range(api_response_tester):
    path = (
        f"{NOM_PATH}&date_naissance_personne_min=2000-01-01"
        "&date_naissance_personne_max=1990-01-01"
    )
    api_response_tester.assert_api_response_code_400(path)
    assert api_response_tester.get_error_message(path) == (
        "Veuillez indiquer une date minimale inférieure à la date maximale."
    )


def test_type_personne_defaults_to_dirigeants_and_elus(api_response_tester):
    sirens = api_response_tester.get_sirens(
        f"search?nom_personne={ELU_NOM}&per_page=25"
    )
    assert COMMUNE_DE_LAMBESC in sirens


def test_type_personne_dirigeant_excludes_elus(api_response_tester):
    path = f"search?nom_personne={ELU_NOM}&type_personne=DIRIGEANT&per_page=25"
    api_response_tester.assert_siren_not_in_results(path, COMMUNE_DE_LAMBESC)
    assert api_response_tester.get_total_results(path) > 0


def test_type_personne_elu_excludes_dirigeants(api_response_tester):
    path = f"{NOM_PATH}&type_personne=ELU"
    assert api_response_tester.get_total_results(path) == 0


def test_type_personne_elu_returns_only_collectivites(api_response_tester):
    results = api_response_tester.get_results(
        "search?nom_personne=martin&type_personne=ELU&per_page=25"
    )
    assert results
    for result in results:
        collectivite = result["complements"]["collectivite_territoriale"]
        assert collectivite is not None, (
            f"{result['siren']} n'est pas une collectivité territoriale."
        )
        assert collectivite["elus"]


def test_type_personne_must_be_valid(api_response_tester):
    path = f"{NOM_PATH}&type_personne=AUTRE"
    api_response_tester.assert_api_response_code_400(path)
    assert "type_personne" in api_response_tester.get_error_message(path)


def test_person_search_combined_with_text_query(api_response_tester):
    path = f"search?q=arcturus&nom_personne={DIRIGEANT_NOM}"
    assert api_response_tester.get_sirens(path) == [ARCTURUS]


def test_person_search_combined_with_filter(api_response_tester):
    all_sirens = set(api_response_tester.get_sirens(f"{NOM_PATH}&per_page=25"))
    filtered_sirens = set(
        api_response_tester.get_sirens(f"{NOM_PATH}&departement=75&per_page=25")
    )
    assert filtered_sirens
    assert filtered_sirens < all_sirens


def test_person_search_never_returns_masked_dirigeants(api_response_tester):
    for nom in ("martin", "bernard", "dupont"):
        results = api_response_tester.get_results(
            f"search?nom_personne={nom}&type_personne=DIRIGEANT&per_page=25"
        )
        assert results
        for result in results:
            assert result["nom_complet"] != MASQUE_NON_DIFFUSIBLE
            for dirigeant in result["dirigeants"]:
                assert dirigeant.get("nom") != MASQUE_NON_DIFFUSIBLE


def test_elu_search_by_prenom_is_accent_insensitive(api_response_tester):
    for prenom in ("helene", "hélène", "HELENE"):
        path = (
            f"search?nom_personne={ELU_NOM}&prenoms_personne={prenom}&type_personne=ELU"
        )
        api_response_tester.assert_siren_in_results(path, COMMUNE_DE_LAMBESC)
