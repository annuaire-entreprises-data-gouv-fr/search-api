from fastapi import APIRouter

from app.service.convention_collective import (
    fetch_idcc_siret_mapping,
    get_metadata_cc_response,
)
from app.service.data_updates import get_last_modified_response

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


@router.get("/metadata/updates")
async def data_updates_endpoint():
    """
    Endpoint for serving data sources' last modified dates JSON file.
    """
    return get_last_modified_response()
