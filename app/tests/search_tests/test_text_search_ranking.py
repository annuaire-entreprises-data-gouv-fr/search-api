import pytest

from app.tests.search_tests.search_fixtures import (
    ARCTURUS,
    CNRS,
    COMMUNE_DE_LAMBESC,
    DENOMINATION_ALLIETTA,
    DIRIGEANT_NOM,
    DIRIGEANT_PRENOM_EXACT,
    EDF,
    EDF_HOMONYME,
    ELU_NOM,
    GANYMEDE,
    LA_POSTE,
    PERSONNE_PHYSIQUE_ALLIETTA,
    PERSONNE_PHYSIQUE_ALLIETTA_NOM_COMPLET,
)

# "ALLIETTA" est à la fois un nom de dénomination, de personne physique, de
#  dirigeant et d'élu : utile pour tester l'algo de recherche.
# Et 2 pages suffisent à couvrir les résultats.
ALLIETTA_PATH = f"search?q={ELU_NOM}&per_page=25"
ALLIETTA_PAGES = 2


def test_denomination_allietta_fixture_is_reachable(api_response_tester):
    api_response_tester.assert_first_siren(
        f"search?q={DENOMINATION_ALLIETTA}", DENOMINATION_ALLIETTA
    )


def test_results_are_sorted_by_decreasing_score(api_response_tester):
    scores = api_response_tester.get_scores("search?q=la poste&per_page=25")
    assert scores == sorted(scores, reverse=True)


def test_exact_denomination_ranks_first(api_response_tester):
    """`exact nom_complet match` (boost 300) domine les autres matchs."""
    api_response_tester.assert_first_siren(ALLIETTA_PATH, DENOMINATION_ALLIETTA)
    api_response_tester.assert_siren_ranked_before(
        ALLIETTA_PATH, DENOMINATION_ALLIETTA, PERSONNE_PHYSIQUE_ALLIETTA
    )


def test_exact_denomination_scores_higher_than_partial_match(api_response_tester):
    exact_score = api_response_tester.get_score_of_siren(
        f"search?q={PERSONNE_PHYSIQUE_ALLIETTA_NOM_COMPLET}",
        PERSONNE_PHYSIQUE_ALLIETTA,
    )
    partial_score = api_response_tester.get_score_of_siren(
        "search?q=jean louis allietta", PERSONNE_PHYSIQUE_ALLIETTA
    )
    assert exact_score > partial_score


def test_denomination_matches_rank_above_person_matches(api_response_tester):
    results = [
        result
        for result in api_response_tester.get_results_over_pages(
            ALLIETTA_PATH, ALLIETTA_PAGES
        )
        if result["nombre_etablissements_ouverts"]
    ]
    matched_on_name = [
        ELU_NOM.upper() in (result["nom_complet"] or "") for result in results
    ]

    assert matched_on_name[0], (
        "La fixture attend une correspondance sur la dénomination en tête."
    )
    assert not all(matched_on_name), (
        "La fixture attend au moins une correspondance par personne seule."
    )

    first_person_match = matched_on_name.index(False)
    sirens_after = [result["siren"] for result in results[first_person_match:]]
    assert not any(matched_on_name[first_person_match:]), (
        "Une correspondance sur la dénomination est classée après une "
        f"correspondance par personne seule. Résultats suivants : {sirens_after}."
    )


def test_elu_match_ranks_below_denomination_matches(api_response_tester):
    results = api_response_tester.get_results_over_pages(ALLIETTA_PATH, ALLIETTA_PAGES)
    sirens = [result["siren"] for result in results]
    assert COMMUNE_DE_LAMBESC in sirens
    assert sirens.index(COMMUNE_DE_LAMBESC) > sirens.index(DENOMINATION_ALLIETTA)


def test_exact_sigle_ranks_first(api_response_tester):
    """`exact sigle match` (boost 100) place le bon CNRS devant les autres."""
    path = "search?q=cnrs"
    api_response_tester.assert_first_siren(path, CNRS)
    scores = api_response_tester.get_scores(path)
    assert scores[0] > scores[1]


def test_nombre_etablissements_ouverts_boosts_ranking(api_response_tester):
    path = "search?q=electricite de france&per_page=25"
    api_response_tester.assert_siren_ranked_before(path, EDF, EDF_HOMONYME)

    results = api_response_tester.get_results(path)
    by_siren = {result["siren"]: result for result in results}
    assert (
        by_siren[EDF]["nombre_etablissements_ouverts"]
        > by_siren[EDF_HOMONYME]["nombre_etablissements_ouverts"]
    )
    assert by_siren[EDF_HOMONYME]["nom_complet"] == "ELECTRICITE DE FRANCE"


def test_address_only_match_ranks_last(api_response_tester):
    path = "search?q=ecole massillon quai des celestins&per_page=25"
    results = api_response_tester.get_results(path)
    address_only = [
        result
        for result in results
        if "MASSILLON" not in (result["nom_complet"] or "")
        and any(
            "MASSILLON" in (etablissement["adresse"] or "")
            for etablissement in result["matching_etablissements"]
        )
    ]
    assert address_only, "Le test attend au moins une correspondance par adresse seule."
    sirens = [result["siren"] for result in results]
    last_name_match = max(
        index
        for index, result in enumerate(results)
        if "MASSILLON" in (result["nom_complet"] or "")
    )
    for result in address_only:
        assert sirens.index(result["siren"]) > last_name_match, (
            "Une correspondance par adresse seule est classée avant une "
            f"correspondance sur la dénomination. Classement : {sirens}."
        )


def test_exact_denomination_beats_larger_network_when_sizes_are_close(
    api_response_tester,
):
    api_response_tester.assert_first_siren("search?q=la poste", LA_POSTE)
    results = api_response_tester.get_results("search?q=la poste&per_page=25")
    assert results[0]["nom_complet"] == "LA POSTE"
    assert results[0]["meta"]["score"] > results[1]["meta"]["score"]


def test_sort_by_size_changes_the_ranking(api_response_tester):
    default_sirens = api_response_tester.get_sirens("search?q=total&per_page=5")
    by_size_sirens = api_response_tester.get_sirens(
        "search?q=total&per_page=5&sort_by_size=true"
    )
    assert default_sirens != by_size_sirens


def test_sort_by_size_prioritises_large_companies(api_response_tester):
    results = api_response_tester.get_results(
        "search?q=total&per_page=5&sort_by_size=true"
    )
    assert results
    for result in results:
        assert result["categorie_entreprise"] in ("GE", "ETI")


def test_sort_by_size_keeps_scores_decreasing(api_response_tester):
    scores = api_response_tester.get_scores(
        "search?q=total&per_page=25&sort_by_size=true"
    )
    assert scores == sorted(scores, reverse=True)


def test_filter_only_search_is_sorted_by_nombre_etablissements(
    api_response_tester,
):
    """
    Sans recherche textuelle, le tri par score est inutile : on trie par nombre d'établissements.
    Voir `ElasticSearchRunner.sort_es_search_query`.
    """
    results = api_response_tester.get_results(
        "search?est_administration=true&per_page=25"
    )
    counts = [result["nombre_etablissements_ouverts"] for result in results]
    assert counts == sorted(counts, reverse=True)


def test_person_filter_search_is_sorted_by_score(api_response_tester):
    scores = api_response_tester.get_scores(
        f"search?nom_personne={DIRIGEANT_NOM}&per_page=25"
    )
    assert scores == sorted(scores, reverse=True)
    assert scores[0] > 0


def test_exact_prenoms_ranks_before_partial_prenoms(api_response_tester):
    path = (
        f"search?nom_personne={DIRIGEANT_NOM}&prenoms_personne={DIRIGEANT_PRENOM_EXACT}"
    )
    api_response_tester.assert_siren_ranked_before(path, ARCTURUS, GANYMEDE)


@pytest.mark.xfail(
    strict=True,
    reason="`sort_by_size` change le nombre d'entités trouvées, alors qu'il ne "
    "devrait changer que leur ordre.",
)
def test_sort_by_size_does_not_change_the_number_of_results(api_response_tester):
    for terms in ("total", "electricite de france", "la poste"):
        default_total = api_response_tester.get_total_results(f"search?q={terms}")
        by_size_total = api_response_tester.get_total_results(
            f"search?q={terms}&sort_by_size=true"
        )
        assert by_size_total == default_total, (
            f"`{terms}` : {default_total} résultats par défaut contre "
            f"{by_size_total} avec `sort_by_size`."
        )
