from datetime import timedelta

from fastapi.responses import JSONResponse

from app.config import settings
from app.utils.cache import cache_strategy
from app.utils.helpers import fetch_json_from_url


def should_cache_for_how_long():
    return timedelta(hours=24)


def get_updates_json():
    return fetch_json_from_url(str(settings.metadata.url_updates_json))


def get_last_modified_response():
    cache_key = "updates_json"
    json_content = cache_strategy(
        cache_key,
        get_updates_json,
        should_cache_for_how_long,
    )
    return JSONResponse(json_content)
