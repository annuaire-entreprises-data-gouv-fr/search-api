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
        return response

    def get_api_response_code(self, path):
        response = self.get_api_response(path)
        return response.status_code

    def assert_api_response_code_200(self, path):
        response_status_code = self.get_api_response_code(path)
        assert (
            response_status_code == ok_status_code
        ), f"API response code is {response_status_code}, expected 200."

    def assert_api_response_code_400(self, path):
        response_status_code = self.get_api_response_code(path)
        assert response_status_code == client_error_status_code, (
            f"API response code is " f"{response_status_code}, expected 400."
        )

    def test_field_value(self, path, result_number, field_name, expected_value):
        response = self.get_api_response(path)
        if response.status_code == ok_status_code:
            # response = response.json()
            response_value = get_field_value(
                response.json()["results"][result_number], field_name
            )
            assert (
                response_value == expected_value
            ), f"Field '{field_name}' has unexpected value."

    def test_number_of_results(self, path, expected_min_count):
        response = self.get_api_response(path)
        if response.status_code == ok_status_code:
            count = response.json()["total_results"]
            assert (
                count >= expected_min_count
            ), f"Expected minimum {expected_min_count} results, but found {count}."
