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


def test_dirigeant_filter():
    path = (
        "search?nom_dirigeant=jouppe&prenoms_dirigeant=xavier "
        "erwan&date_naissance_dirigeant_min=1970-01-01"
        "&date_naissance_dirigeant_max"
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
    path = "search?date_naissance_dirigeant_min=13/09/2001"
    response = requests.get(url=base_url + path)
    assert response.status_code == 400


def test_error_query():
    path = "search?qs=ganymede"
    response = requests.get(url=base_url + path)
    assert response.status_code == 400
