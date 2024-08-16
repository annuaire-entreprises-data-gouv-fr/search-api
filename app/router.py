from fastapi import APIRouter, Request

from app.request.search_type import SearchType
from app.response.admin_endpoint.convention_collective import (
    fetch_idcc_siret_mapping,
    get_metadata_cc_response,
)
from app.response.build_api_response import build_api_response

router = APIRouter()


@router.get("/search")
async def search_text_endpoint(request: Request):
    return build_api_response(
        request,
        search_type=SearchType.TEXT,
    )


@router.get("/near_point")
async def near_point_endpoint(request: Request):
    return build_api_response(
        request,
        search_type=SearchType.GEO,
    )


@router.get("/idcc/metadata")
async def conventions_collectives_endpoint():
    """
    Endpoint for serving the convention collective JSON file.
    """
    return get_metadata_cc_response()


@router.get("/idcc/{siren}")
async def search_conventions_collectives_by_siren_endpoint(siren: str):
    """
    Endpoint for searching conventions collectives by SIREN number.
    """
    return fetch_idcc_siret_mapping(siren)
