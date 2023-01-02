import json
import os
from typing import Callable, Dict

from aio_proxy.decorators.http_exception import http_exception_handler
from aio_proxy.response.format_response import format_response
from aio_proxy.search.index import ElasticsearchSireneIndex
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV")


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
    total_results, results, execution_time = search_function(
        ElasticsearchSireneIndex, page * per_page, per_page, **parameters
    )
    results_formatted = format_response(results)
    res = {
        "results": results_formatted,
        "total_results": int(total_results),
        "page": page + 1,
        "per_page": per_page,
    }
    remainder_results = res["total_results"] % res["per_page"]
    res["total_pages"] = (
        res["total_results"] // res["per_page"]
        if remainder_results == 0
        else res["total_results"] // res["per_page"] + 1
    )

    if env == "dev":
        res["execution_time"] = execution_time
    return web.json_response(text=json.dumps(res, default=str))
