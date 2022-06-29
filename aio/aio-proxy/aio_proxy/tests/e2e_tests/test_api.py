# importing the requests library
import requests
import logging

# api-endpoint
base_url = "http://localhost:4500/"


def test_fetch_company():
    path = "search?q=la poste"
    response = requests.get(url=base_url + path)
    response_json = response.json()
    total_results = response_json["total_results"]
    siren = response_json["results"][0]["siren"]
    logging.info(f"****** siren de la poste: {siren} ******")
    assert response.status_code == 200
    assert total_results > 10
    assert siren == "356000000"


def test_error_query():
    path = "search?qs=ganymede"
    response = requests.get(url=base_url + path)
    assert response.status_code == 400
