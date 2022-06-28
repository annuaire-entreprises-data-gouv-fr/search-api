# importing the requests library
import requests

# api-endpoint
base_url = "http://localhost:4500/"


def test_fetch_company():
    path = "search?q=ganymede"
    response = requests.get(url=base_url+path)
    assert response.status_code == 200


def test_error():
    path = "search?qs=ganymede"
    response = requests.get(url=base_url+path)
    # response_json = json.loads(response.text)
    assert response.status_code == 400
