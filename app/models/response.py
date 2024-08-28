from pydantic import BaseModel, RootModel

from app.models.unite_legale import UniteLegaleResponse


class ResponseModel(BaseModel):
    results: list[UniteLegaleResponse] | None = None
    total_results: int = None
    page: int = None
    per_page: int = None
    total_pages: int = None
    execution_time: int | None = None


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
