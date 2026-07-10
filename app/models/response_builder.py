from typing import ClassVar

from app.models.response import PaginatedResponseModel, ResponseModel
from app.service.format_search_results import format_search_results
from app.utils.helpers import is_dev_env


class PaginatedResponseBuilder:
    """
    Build the paginated API response common to all search types.
    Subclasses must set response_model and implement format_results().
    """

    response_model: ClassVar[type[PaginatedResponseModel]]

    def __init__(self, search_params, es_search_results):
        self.total_results = min(int(es_search_results.total_results), 10000)
        self.per_page = search_params.per_page
        self.results = self.format_results(
            es_search_results.es_search_results, search_params
        )
        self.page = search_params.page
        self.total_pages = self.calculate_total_pages()
        response = self.response_model(
            results=self.results,
            total_results=self.total_results,
            page=self.page,
            per_page=self.per_page,
            total_pages=self.total_pages,
        )
        if is_dev_env():
            response.execution_time = es_search_results.execution_time
        self.response = response.dict(exclude_unset=True, by_alias=True)

    def format_results(self, results, search_params):
        raise NotImplementedError

    def calculate_total_pages(self):
        quotient, remainder = divmod(
            self.total_results,
            self.per_page,
        )
        return quotient + 1 if remainder > 0 else quotient


class ResponseBuilder(PaginatedResponseBuilder):
    response_model = ResponseModel

    def format_results(self, results, search_params):
        return format_search_results(results, search_params)
