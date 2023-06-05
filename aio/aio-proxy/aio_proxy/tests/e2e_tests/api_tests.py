import pytest
import requests
from requests.adapters import HTTPAdapter, Retry

ok_status_code = 200
client_error_status_code = 400
min_total_results = 10
min_total_results_filters = 1000


def get_field_value(results, field_name):
    fields = field_name.split(".")
    value = results
    for f in fields:
        if isinstance(value, dict) and f in value:
            value = value[f]
        elif isinstance(value, list):
            try:
                index = int(f)
                value = value[index]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return value


class APIResponseTester:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_api_response(self, path):
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=3)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get(url=self.api_url + path)
        return response.json()

    def assert_api_response_code_200(self, path):
        response = self.get_api_response(path)
        assert (
            response.status_code == ok_status_code
        ), f"API response code is {response.status_code}, expected 200."

    def test_client_error_response(self, path):
        response = self.get_api_response(path)
        assert response.status_code == client_error_status_code, (
            f"API response code is " f"{response.status_code}, expected 400."
        )

    def test_field_value(self, path, field_name, expected_value):
        response = self.get_api_response(path)
        if response.status_code == ok_status_code:
            response_value = get_field_value(response["results"][0], field_name)
            assert (
                response_value == expected_value
            ), f"Field '{field_name}' has unexpected value."

    def test_number_of_results(self, path, expected_min_count):
        response = self.get_api_response(path)
        if response.status_code == ok_status_code:
            count = response["total_results"]
            assert (
                count >= expected_min_count
            ), f"Expected minimum {expected_min_count} results, but found {count}."


@pytest.fixture
def api_response_tester():
    api_url = "http://localhost:4500/"
    return APIResponseTester(api_url)


def test_api_response_fields(api_response_tester):
    api_response_tester.test_field_value("field1", "value1")
    api_response_tester.test_field_value("field2", "value2")
    # Add more field tests as needed


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
    api_response_tester.test_client_error_response(path)


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
    api_response_tester.test_client_error_response(path)


def test_query_too_short(api_response_tester):
    """
    test if API returns an error for a two character query
    """
    path = "search?q=ab"
    api_response_tester.test_client_error_response(path)


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
    api_response_tester.test_client_error_response(path)


def test_bool_filters(api_response_tester):
    """
    test if using "est_rge" and "convention_collective_renseignee" filters returns only
    établissements` with `rge` and `convention collective` ids.
    """
    path = "search?convention_collective_renseignee=true&est_rge=true"
    api_response_tester.test_number_of_results(path, 1)
    api_response_tester.test_field_value(path, "complements.est_rge", True)
    api_response_tester.test_field_value(
        path, "complements.convention_collective_renseignee", True
    )
    api_response_tester.test_field_value(
        path, "matching_etablissements.0.liste_idcc", True
    )
