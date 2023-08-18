from aio_proxy.response.format_search_results import format_search_results
from aio_proxy.response.helpers import is_dev_env


class ResponseBuilder:
    def __init__(self, search_params, es_search_results):
        self.total_results = es_search_results.total_results
        self.search_results = es_search_results.es_search_results
        self.execution_time = es_search_results.execution_time
        self.search_params = search_params
        self.response = self.format_response()

    def format_response(self):
        formatted_search_results = format_search_results(
            self.search_results, self.search_params
        )
        response = {
            "results": formatted_search_results,
            "total_results": min(int(self.total_results), 10000),
            "page": self.search_params.page + 1,
            "per_page": self.search_params.per_page,
            "total_pages": self.calculate_total_pages(),
        }
        if is_dev_env():
            response["execution_time"] = self.execution_time
        return response

    def calculate_total_pages(self):
        total_pages, remainder = divmod(
            self.total_results,
            self.search_params.per_page,
        )
        if remainder > 0:
            total_pages += 1
        return total_pages
