from datetime import timedelta

from fastapi.responses import JSONResponse

from app.config import settings
from app.utils.cache import cache_strategy
from app.utils.helpers import fetch_json_from_url

TIME_TO_LIVE = timedelta(days=1)


def should_cache_search_response():
    return True


def get_updates_json():
    return fetch_json_from_url(str(settings.metadata.url_updates_json))


def get_last_modified_response():
    cache_key = "updates_json"
    json_content = cache_strategy(
        cache_key,
        get_updates_json,
        should_cache_search_response,
        TIME_TO_LIVE,
    )
    return JSONResponse(json_content)
