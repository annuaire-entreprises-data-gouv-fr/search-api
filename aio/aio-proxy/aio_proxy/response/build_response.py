import json
import logging

from aio_proxy.request.search_params_builder import SearchParamsBuilder
from aio_proxy.response.format_response import ResponseBuilder
from aio_proxy.search.es_search_runner import ElasticSearchRunner
from aiohttp import web
from sentry_sdk import capture_exception, push_scope


# @http_exception_handler
def api_response(
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
    try:
        search_params = SearchParamsBuilder.extract_params(request, search_type)
        es_search_results = ElasticSearchRunner(search_params, search_type)
        formatted_response = ResponseBuilder(search_params, es_search_results)
        return web.json_response(
            text=json.dumps(formatted_response.response, default=str)
        )
    except ValueError as error:
        with push_scope() as scope:
            # group value errors together based on their response (Bad request)
            scope.fingerprint = ["Bad Request"]
            # capture_exception(error)
            logging.warning(f"Bad request: {error}")
            raise error
    # capture error in Sentry
    except Exception as error:
        # capturing error at this level allows us to get the actual error before it's
        # wrapped in http_exception_handler
        capture_exception(error)
        raise error
