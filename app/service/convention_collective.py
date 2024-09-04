import os
from datetime import timedelta

from fastapi.responses import JSONResponse

from app.elastic.parsers.siren import is_siren
from app.elastic.queries.search_by_siren import search_index_by_siren
from app.exceptions.exceptions import InvalidSirenError
from app.models.response import CcResponseModel
from app.service.formatters.convention_collective import (
    extract_idcc_siret_mapping_from_ul,
)
from app.utils.cache import cache_strategy
from app.utils.helpers import fetch_json_from_url

TIME_TO_LIVE = timedelta(days=1)
URL_CC_JSON = os.getenv("METADATA_URL_CC_JSON")


def should_cache_search_response():
    return True


def get_metadata_json():
    return fetch_json_from_url(URL_CC_JSON)


def get_metadata_cc_response():
    cache_key = "cc_kali_json"
    json_content = cache_strategy(
        cache_key,
        get_metadata_json,
        should_cache_search_response,
        TIME_TO_LIVE,
    )
    return JSONResponse(json_content)


def fetch_idcc_siret_mapping(siren):
    """
    Retrieves the detailed list of SIRET numbers associated with an IDCC for a
    given SIREN number.

    Args:
        request : The HTTP request object containing 'siren'
        in match_info.

    Returns:
        Response: response containing the list of IDCCs or an empty
        list if no match found.

    Raises:
        ValueError: If the SIREN number is invalid.
    """
    if not is_siren(siren):
        raise InvalidSirenError()

    match_siren = search_index_by_siren(siren)

    if not match_siren:
        return JSONResponse({})

    idcc_mapping = extract_idcc_siret_mapping_from_ul(match_siren)

    response_data = CcResponseModel(root=idcc_mapping)
    return response_data