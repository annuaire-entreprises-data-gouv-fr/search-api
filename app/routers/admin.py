from fastapi import APIRouter

from app.response.admin_endpoint.convention_collective import (
    fetch_idcc_siret_mapping,
    get_metadata_cc_response,
)

router = APIRouter()


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
