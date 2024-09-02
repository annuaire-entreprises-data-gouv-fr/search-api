from fastapi.responses import ORJSONResponse

from app.controller.search_params_builder import SearchParamsBuilder
from app.decorators.http_exception import http_exception_handler
from app.elastic.es_search_runner import ElasticSearchRunner
from app.models.response_builder import ResponseBuilder
from app.utils.matomo import track_event


@http_exception_handler
def build_api_response(
    request,
    search_type,
) -> dict[str, int]:
    """Create and format API response.

    Args:
        request: HTTP request.
        search_type: type of search.
    Returns:
        response in json format (results, total_results, page, per_page,
        total_pages)
    """
    track_event(request)
    search_params = SearchParamsBuilder.extract_params(request, search_type)
    es_search_results = ElasticSearchRunner(search_params, search_type)
    formatted_response = ResponseBuilder(search_params, es_search_results)
    return ORJSONResponse(content=formatted_response.response)
