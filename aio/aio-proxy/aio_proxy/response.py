import json
from typing import Callable, Dict

from aio_proxy.helpers import hide_fields, serialize_error_text
from aio_proxy.search.index import Siren
from aiohttp import web

import elasticsearch


def api_response(
    request, extract_function: Callable, search_function: Callable
) -> Dict[str, int]:
    try:
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
        return res
    except (elasticsearch.exceptions.RequestError, ValueError, TypeError) as error:
        raise web.HTTPBadRequest(
            text=serialize_error_text(str(error)), content_type="application/json"
        )
    except BaseException as error:
        raise web.HTTPInternalServerError(
            text=serialize_error_text(str(error)), content_type="application/json"
        )
