from typing import Generic, TypeVar

from pydantic import BaseModel, RootModel

from app.models.fondation import FondationResponse
from app.models.unite_legale import UniteLegaleResponse

ResultType = TypeVar("ResultType")


class PaginatedResponseModel(BaseModel, Generic[ResultType]):
    results: list[ResultType] | None = None
    total_results: int | None = None
    page: int | None = None
    per_page: int | None = None
    total_pages: int | None = None
    execution_time: int | None = None


ResponseModel = PaginatedResponseModel[UniteLegaleResponse]
FondationResponseModel = PaginatedResponseModel[FondationResponse]


class CcResponseModel(RootModel):
    """
    A model representing the response structure for IDCC to SIRET mapping.

    Attributes:
        root (dict): A dictionary where keys are IDCC strings and values are lists of
        SIRET strings.
            Example:
            {
                "7002": ["77557501200486", "77557501200445"],
                "1077": ["77557501200916"]
            }
    """

    root: dict[str, list[str]]
