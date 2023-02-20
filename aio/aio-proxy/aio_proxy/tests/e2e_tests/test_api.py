# importing the requests library
import requests
from requests.adapters import HTTPAdapter, Retry

# api-endpoint
base_url = "http://localhost:4500/"

session = requests.Session()
retry = Retry(connect=3, backoff_factor=3)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

ok_status_code = 200
client_error_status_code = 400
min_total_results_la_poste = 10
min_total_results_service_public = 1000


def test_fetch_company():
    """
    test if searching for `la poste` returns the right siren as the first search result.
    """
    path = "search?q=la poste"
    response = session.get(url=base_url + path)
    response_json = response.json()
    total_results = response_json["total_results"]
    siren = response_json["results"][0]["siren"]
    print(response)
    assert response.status_code == ok_status_code
    assert total_results > min_total_results_la_poste
    assert siren == "356000000"


def test_personne_filter():
    """
    test if using `personne` filters returns the right siren (ganymede)
    """
    path = (
        "search?nom_personne=jouppe&prenoms_personne=xavier erwan"
        "&date_naissance_personne_min=1970-01-01"
        "&date_naissance_personne_max"
        "=2000-01-01"
    )
    response = session.get(url=base_url + path)
    response_json = response.json()
    total_results = response_json["total_results"]
    siren = response_json["results"][0]["siren"]
    assert response.status_code == ok_status_code
    assert total_results == 1
    assert siren == "880878145"


def test_format_date_naissance():
    """
    test if using the wrong date of birth returns an error.
    """
    path = "search?date_naissance_personne_min=13/09/2001"
    response = session.get(url=base_url + path)
    assert response.status_code == client_error_status_code


def test_error_query():
    """
    test if giving wrong query parameters returns an error.
    """
    path = "search?qs=ganymede"
    response = session.get(url=base_url + path)
    assert response.status_code == client_error_status_code


def test_accept_three_characters():
    """
    test if API returns results for a three character query.
    """
    path = "search?q=abc"
    response = session.get(url=base_url + path)
    assert response.status_code == ok_status_code


def test_query_too_short():
    """
    test if API returns an error for a two character query
    """
    path = "search?q=ab"
    response = session.get(url=base_url + path)
    assert response.status_code == client_error_status_code


def test_short_query_with_filter():
    """
    test if using a filter with a two character query returns results.
    """
    path = "search?q=ab&code_postal=75015"
    response = session.get(url=base_url + path)
    print(response.text)
    assert response.status_code == ok_status_code


def test_terms_empty_only():
    """
    test if searching using empty search parameters returns an error.
    """
    path = "search?q="
    response = session.get(url=base_url + path)
    assert response.status_code == client_error_status_code


def test_bool_filters():
    """
    test if using "est_rge" and "convention_collective_renseignee" filters returns only
    établissements` with `rge` and `convention collective` ids.
    """
    path = "search?convention_collective_renseignee=true&est_rge=true"
    response = session.get(url=base_url + path)
    response_json = response.json()
    total_results = response_json["total_results"]
    est_rge = response_json["results"][0]["complements"]["est_rge"]
    cc_renseignee = response_json["results"][0]["complements"][
        "convention_collective_renseignee"
    ]
    liste_rge = response_json["results"][0]["matching_etablissements"][0]["liste_rge"]
    liste_cc = response_json["results"][0]["matching_etablissements"][0]["liste_idcc"]
    assert response.status_code == ok_status_code
    assert est_rge
    assert cc_renseignee
    assert liste_rge
    assert liste_cc
    assert total_results > 1


def test_est_service_public():
    """
    test if `est_service_public`  filter returns results with and without text search.
    """
    path_filter_only = "search?est_service_public=true"
    response_filters_only = session.get(url=base_url + path_filter_only)
    total_results = response_filters_only.json()["total_results"]
    path_filter_with_text = "search?est_service_public=true&q=ministere"
    response_filters_with_text = session.get(url=base_url + path_filter_with_text)
    assert response_filters_only.status_code == ok_status_code
    assert total_results > min_total_results_service_public
    assert response_filters_with_text.status_code == ok_status_code


def test_min_per_page():
    """
    test if giving a per_page smaller than 0, return a value error
    """
    path = "search?q=ganymede&per_page=0"
    response = session.get(url=base_url + path)
    assert response.status_code == client_error_status_code
