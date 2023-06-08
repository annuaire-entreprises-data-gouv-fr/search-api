import pytest
from aio_proxy.tests.e2e_tests.response_tester import APIResponseTester

min_total_results = 10
min_total_results_filters = 1000


@pytest.fixture
def api_response_tester():
    api_url = "http://localhost:4500/"
    return APIResponseTester(api_url)


def test_fetch_company(api_response_tester):
    """
    test if searching for `la poste` returns the right siren as the first search result.
    """
    path = "search?q=la poste"
    api_response_tester.test_field_value(path, "siren", "356000000")
    api_response_tester.test_number_of_results(path, min_total_results)


def test_personne_filter(api_response_tester):
    """
    test if using `personne` filters returns the right siren (ganymede)
    """
    path = (
        "search?nom_personne=jouppe&prenoms_personne=xavier erwan"
        "&date_naissance_personne_min=1970-01-01"
        "&date_naissance_personne_max"
        "=2000-01-01"
    )
    api_response_tester.test_field_value(path, "siren", "880878145")
    api_response_tester.test_number_of_results(path, 1)


def test_error_query(api_response_tester):
    """
    test if giving wrong query parameters returns an error.
    """
    path = "search?qs=ganymede"
    api_response_tester.assert_api_response_code_400(path)


def test_accept_three_characters(api_response_tester):
    """
    test if API returns results for a three character query.
    """
    path = "search?q=abc"
    api_response_tester.assert_api_response_code_200(path)


def test_format_date_naissance(api_response_tester):
    """
    test if using the wrong date of birth returns an error.
    """
    path = "search?date_naissance_personne_min=13/09/2001"
    api_response_tester.assert_api_response_code_400(path)


def test_query_too_short(api_response_tester):
    """
    test if API returns an error for a two character query
    """
    path = "search?q=ab"
    api_response_tester.assert_api_response_code_400(path)


def test_short_query_with_filter(api_response_tester):
    """
    test if using a filter with a two character query returns results.
    """
    path = "search?q=ab&code_postal=75015"
    api_response_tester.assert_api_response_code_200(path)


def test_terms_empty_only(api_response_tester):
    """
    test if searching using empty search parameters returns an error.
    """
    path = "search?q="
    api_response_tester.assert_api_response_code_400(path)


def test_bool_filters(api_response_tester):
    """
    test if using "est_rge" and "convention_collective_renseignee" filters returns only
    établissements` with `rge` and `convention collective` ids.
    """
    path = "search?convention_collective_renseignee=true&est_rge=true"
    api_response_tester.test_number_of_results(path, 1)
    api_response_tester.test_field_value(path, "complements.est_rge", True)
    """
    api_response_tester.test_field_value(
        path, "complements.convention_collective_renseignee", True
    )
    api_response_tester.test_field_value(
        path, "matching_etablissements.0.liste_idcc", True
    )
    """


def test_organisme_formation(api_response_tester):
    """
    test est_organisme_formation et est_qualiopi
    """
    path = "search?est_organisme_formation=true&est_qualiopi=true"
    api_response_tester.test_number_of_results(path, min_total_results_filters)


def test_near_point(api_response_tester):
    """
    test near point endpoint
    """
    path = "near_point?lat=48&long=2&radius=5"
    api_response_tester.assert_api_response_code_200(path)


def test_categorie_entreprise_list(api_response_tester):
    """
    test categorie_entreprise filter
    """
    path = "search?categorie_entreprise=GE,PME"
    api_response_tester.assert_api_response_code_200(path)


def test_banned_param(api_response_tester):
    """
    test if banned param returns a 400 status code.
    """
    path = "search?localisation=45000"
    api_response_tester.assert_api_response_code_400(path)


def test_siren_search(api_response_tester):
    """
    test if valid `siren` search returns results
    """
    path = "search?q=130025265"
    api_response_tester.assert_api_response_code_200(path)
    api_response_tester.test_field_value(path, "siren", "130025265")


def test_page_number(api_response_tester):
    """
    test if giving a page number higher than 1000 returns a value error
    """
    path = "search?q=ganymede&page=10001"
    api_response_tester.assert_api_response_code_400(path)


def test_min_per_page(api_response_tester):
    """
    test if giving a per_page smaller than 0, return a value error
    """
    path = "search?q=ganymede&per_page=0"
    api_response_tester.assert_api_response_code_400(path)


def test_est_service_public(api_response_tester):
    """
    test if `est_service_public`  filter returns results with and without text search.
    """
    path = "search?est_service_public=true"
    api_response_tester.test_number_of_results(path, min_total_results_filters)
    api_response_tester.test_field_value(path, "complements.est_service_public", True)
    path = "search?est_service_public=true&q=ministere"
    api_response_tester.test_field_value(path, "complements.est_service_public", True)


def test_societe_a_mission(api_response_tester):
    """
    test est_societe_mission
    """
    path = "search?est_societe_mission=true"
    api_response_tester.test_number_of_results(path, 500)
    api_response_tester.test_field_value(path, "complements.est_societe_mission", True)


def test_commune_filter(api_response_tester):
    path = "search?code_commune=35235"
    api_response_tester.test_field_value(
        path, "matching_etablissements.0.commune", "35235"
    )


def test_activite_principale_filter(api_response_tester):
    path = "search?activite_principale=01.12Z"
    api_response_tester.test_field_value(path, "activite_principale", "01.12Z")


def test_categorie_entreprise(api_response_tester):
    path = "search?categorie_entreprise=PME"
    api_response_tester.test_field_value(path, "categorie_entreprise", "PME")
