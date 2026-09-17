import requests
from requests.adapters import HTTPAdapter, Retry

ok_status_code = 200
client_error_status_code = 400
no_content_status_code = 204
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
        self.api_url = api_url.rstrip("/")

    def get_api_response(self, path):
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=3)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get(url=f"{self.api_url}/{path.lstrip('/')}")
        return response

    def get_api_response_code(self, path):
        response = self.get_api_response(path)
        return response.status_code

    def assert_api_response_code_200(self, path):
        response_status_code = self.get_api_response_code(path)
        assert response_status_code == ok_status_code, (
            f"API response code is {response_status_code}, expected 200."
        )

    def assert_api_response_code_400(self, path):
        response_status_code = self.get_api_response_code(path)
        assert response_status_code == client_error_status_code, (
            f"API response code is {response_status_code}, expected 400."
        )

    def assert_api_response_code_204(self, path):
        response_status_code = self.get_api_response_code(path)
        assert response_status_code == no_content_status_code, (
            f"API response code is {response_status_code}, expected 204."
        )

    def test_field_value(self, path, result_number, field_name, expected_value):
        response = self.get_api_response(path)
        if response.status_code == ok_status_code:
            # response = response.json()
            response_value = get_field_value(
                response.json()["results"][result_number], field_name
            )
            assert response_value == expected_value, (
                f"Field '{field_name}' has unexpected value."
            )

    def test_number_of_results(self, path, expected_min_count):
        response = self.get_api_response(path)
        if response.status_code == ok_status_code:
            count = response.json()["total_results"]
            assert count >= expected_min_count, (
                f"Expected minimum {expected_min_count} results, but found {count}."
            )

    def test_max_number_of_results(self, path, expected_max_count):
        response = self.get_api_response(path)
        if response.status_code == ok_status_code:
            count = response.json()["total_results"]
            assert count <= expected_max_count, (
                f"Expected maximum {expected_max_count} results, but found {count}."
            )

    def test_field_not_none(self, path, result_number, field_name):
        response = self.get_api_response(path)
        if response.status_code == ok_status_code:
            response_value = get_field_value(
                response.json()["results"][result_number], field_name
            )
            assert response_value is not None, (
                f"Field '{field_name}' is None, expected a value."
            )

    def get_json(self, path):
        response = self.get_api_response(path)
        assert response.status_code == ok_status_code, (
            f"API response code is {response.status_code}, expected 200 for `{path}`."
        )
        return response.json()

    def get_results(self, path):
        return self.get_json(path)["results"]

    def get_total_results(self, path):
        return self.get_json(path)["total_results"]

    def get_sirens(self, path):
        return [result["siren"] for result in self.get_results(path)]

    def get_scores(self, path):
        return [result["meta"]["score"] for result in self.get_results(path)]

    def get_results_over_pages(self, path, number_of_pages):
        """Concatenate the results of the specified number of pages, in order.
        `path` must not already carry a `page` parameter.
        """
        results = []
        for page in range(1, number_of_pages + 1):
            separator = "&" if "?" in path else "?"
            results += self.get_results(f"{path}{separator}page={page}")
        return results

    def get_error_message(self, path):
        return self.get_api_response(path).json()["erreur"]

    def get_score_of_siren(self, path, siren):
        for result in self.get_results(path):
            if result["siren"] == siren:
                return result["meta"]["score"]
        raise AssertionError(f"Siren {siren} is not in the results of `{path}`.")

    def assert_first_siren(self, path, siren):
        sirens = self.get_sirens(path)
        assert sirens, f"No result at all for `{path}`."
        assert sirens[0] == siren, (
            f"Expected siren {siren} as first result of `{path}`, "
            f"found {sirens[0]}. Full list: {sirens}."
        )

    def assert_siren_in_results(self, path, siren, limit=None):
        sirens = self.get_sirens(path)
        searched_sirens = sirens if limit is None else sirens[:limit]
        assert siren in searched_sirens, (
            f"Expected siren {siren} in the results of `{path}`. Got: {searched_sirens}."
        )

    def assert_siren_not_in_results(self, path, siren):
        sirens = self.get_sirens(path)
        assert siren not in sirens, (
            f"Siren {siren} should not be returned by `{path}`. Got: {sirens}."
        )

    def assert_siren_ranked_before(self, path, first_siren, second_siren):
        sirens = self.get_sirens(path)
        for siren in (first_siren, second_siren):
            assert siren in sirens, (
                f"Siren {siren} is missing from the results of `{path}`. Got {sirens}."
            )
        assert sirens.index(first_siren) < sirens.index(second_siren), (
            f"Expected siren {first_siren} to rank before {second_siren} "
            f"for `{path}`. Full list ranked: {sirens}."
        )
