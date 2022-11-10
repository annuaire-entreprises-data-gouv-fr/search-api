# importing the requests library
import requests

# api-endpoint
base_url = "http://localhost:4500/"


def test_fetch_company():
    path = "search?q=la poste"
    response = requests.get(url=base_url + path)
    response_json = response.json()
    total_results = response_json["total_results"]
    siren = response_json["results"][0]["siren"]
    assert response.status_code == 200
    assert total_results > 10
    assert siren == "356000000"


def test_personne_filter():
    path = (
        "search?nom=jouppe&prenoms=xavier erwan"
        "&date_naissance_min=1970-01-01"
        "&date_naissance_max"
        "=2000-01-01"
    )
    response = requests.get(url=base_url + path)
    response_json = response.json()
    total_results = response_json["total_results"]
    siren = response_json["results"][0]["siren"]
    assert response.status_code == 200
    assert total_results == 1
    assert siren == "880878145"


def test_format_date_naissance():
    path = "search?date_naissance_min=13/09/2001"
    response = requests.get(url=base_url + path)
    assert response.status_code == 400


def test_error_query():
    path = "search?qs=ganymede"
    response = requests.get(url=base_url + path)
    assert response.status_code == 400


def test_accept_three_characters():
    path = "search?q=abc"
    response = requests.get(url=base_url + path)
    assert response.status_code == 200


def test_query_too_short():
    path = "search?q=ab"
    response = requests.get(url=base_url + path)
    assert response.status_code == 400


def test_short_query_with_filter():
    path = "search?q=ab&code_postal=75015"
    response = requests.get(url=base_url + path)
    assert response.status_code == 200


def test_terms_empty_only():
    path = "search?q="
    response = requests.get(url=base_url + path)
    assert response.status_code == 400
