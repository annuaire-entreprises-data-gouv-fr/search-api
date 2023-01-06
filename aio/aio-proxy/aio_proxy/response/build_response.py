import json
from typing import Callable, Dict

from aio_proxy.decorators.http_exception import http_exception_handler
from aio_proxy.response.format_response import format_response
from aio_proxy.response.format_search_results import format_search_results
from aio_proxy.search.index import ElasticsearchSireneIndex
from aiohttp import web


@http_exception_handler
def api_response(
    request, extract_function: Callable, search_function: Callable
) -> Dict[str, int]:
    """Create and format API response.

    Args:
        request: HTTP request.
        extract_function (Callable): function used to extract parameters.
        search_function (Callable): function used for search .
    Returns:
        response in json format (results, total_results, page, per_page,
        total_pages)
    """
    parameters, page, per_page = extract_function(request)
    total_results, results, execution_time, include_etablissements = search_function(
        ElasticsearchSireneIndex, page * per_page, per_page, **parameters
    )
    results_formatted = format_search_results(results, include_etablissements)
    response_formatted = format_response(
        results_formatted, total_results, page, per_page, execution_time
    )

    return web.json_response(text=json.dumps(response_formatted, default=str))
