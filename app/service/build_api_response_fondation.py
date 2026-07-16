from app.controller.fondation_params_builder import FondationParamsBuilder
from app.elastic.fondation_runner import FondationRunner
from app.models.fondation_response_builder import FondationResponseBuilder
from app.utils.matomo import track_event


def build_api_response_fondation(request) -> dict:
    """Create and format the fondation API response.

    Args:
        request: HTTP request.

    Returns:
        response in json format (results, total_results, page, per_page,
        total_pages)
    """
    track_event(request)
    search_params = FondationParamsBuilder.extract_params(request)
    es_search_results = FondationRunner(search_params)
    formatted_response = FondationResponseBuilder(search_params, es_search_results)
    return formatted_response.response
