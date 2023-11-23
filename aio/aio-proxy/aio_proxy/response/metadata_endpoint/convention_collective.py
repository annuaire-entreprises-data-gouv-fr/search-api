import os
from datetime import timedelta

from aio_proxy.decorators.http_exception import http_exception_handler
from aio_proxy.utils.cache import cache_strategy
from aio_proxy.utils.helpers import fetch_json_from_url
from aiohttp import web

TIME_TO_LIVE = timedelta(days=1)
URL_CC_JSON = os.getenv("METADATA_URL_CC_JSON")


def should_cache_search_response():
    return True


def get_metadata_json():
    return fetch_json_from_url(URL_CC_JSON)


@http_exception_handler
def get_metadata_cc_response():
    cache_key = "cc_kali_json"
    json_content = cache_strategy(
        cache_key,
        get_metadata_json,
        should_cache_search_response,
        TIME_TO_LIVE,
    )
    return web.json_response(json_content)
