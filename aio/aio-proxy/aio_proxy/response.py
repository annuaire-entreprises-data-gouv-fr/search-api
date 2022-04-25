import json
from typing import Callable, Dict

from aio_proxy.decorators.http_exception import http_exception_handler
from aio_proxy.search.helpers import hide_fields
from aio_proxy.search.index import Siren
from aiohttp import web


@http_exception_handler
def api_response(
    request, extract_function: Callable, search_function: Callable
) -> Dict[str, int]:
    parameters, page, per_page = extract_function(request)
    total_results, unite_legale = search_function(
        Siren, page * per_page, per_page, **parameters
    )
    unite_legale_filtered = hide_fields(unite_legale)
    res = {
        "unite_legale": unite_legale_filtered,
        "total_results": int(total_results),
        "page": page + 1,
        "per_page": per_page,
    }
    res["total_pages"] = int(res["total_results"] / res["per_page"]) + 1
    return web.json_response(text=json.dumps([res], default=str))
