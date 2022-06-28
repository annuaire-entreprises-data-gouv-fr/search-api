# importing the requests library
import requests
import json
from jsonpath_ng import jsonpath, parse

# api-endpoint
base_url = "http://localhost:4500/"


def test_fetch_company():
    path = "search?q=ganymede"
    response = requests.get(url=base_url+path)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert jsonpath.jsonpath(response_json, '$.total_results') > 10


def test_error_query():
    path = "search?qs=ganymede"
    response = requests.get(url=base_url+path)
    assert response.status_code == 400
