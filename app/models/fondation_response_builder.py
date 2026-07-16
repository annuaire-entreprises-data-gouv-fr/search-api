from app.models.response import FondationResponseModel
from app.models.response_builder import PaginatedResponseBuilder
from app.service.formatters.fondation import format_fondation_results


class FondationResponseBuilder(PaginatedResponseBuilder):
    response_model = FondationResponseModel

    def format_results(self, results, search_params):
        return format_fondation_results(results, search_params)
