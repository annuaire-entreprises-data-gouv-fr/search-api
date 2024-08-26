from fastapi import APIRouter, Request

from app.request.search_type import SearchType
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
