from aio_proxy.response.unite_legale_model import UniteLegaleResponse
from pydantic import BaseModel


class ResponseModel(BaseModel):
    results: list[UniteLegaleResponse] | None = None
    total_results: int = None
    page: int = None
    per_page: int = None
    total_pages: int = None
    execution_time: int | None = None
