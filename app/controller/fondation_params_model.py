from pydantic import BaseModel, field_validator, model_validator

from app.controller.field_validation import FIELD_LENGTHS, NUMERIC_FIELD_LIMITS
from app.exceptions.exceptions import InvalidParamError


class FondationParams(BaseModel):
    """Class for modeling the fondation parameters"""

    terms: str | None = None
    page: int = 1
    per_page: int = 10

    @field_validator("page", "per_page", mode="before")
    def cast_as_integer(cls, value: str, info) -> int:
        try:
            return int(value)
        except ValueError:
            raise InvalidParamError(
                f"Veuillez indiquer un paramètre `{info.field_name}` entier."
            )

    @field_validator("page", "per_page", mode="after")
    def check_if_number_in_range(cls, value: int, info) -> int:
        limits = NUMERIC_FIELD_LIMITS[info.field_name]
        if value < limits["min"] or value > limits["max"]:
            raise InvalidParamError(
                f"Veuillez indiquer un paramètre `{info.field_name}` entre "
                f"`{limits['min']}` et `{limits['max']}`, "
                f"par défaut `{limits['default']}`."
            )
        return value

    @field_validator("terms", mode="before")
    def make_uppercase(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def check_if_all_empty_params(self):
        """terms parameter is required, fondations have no other filter"""
        if self.terms is None:
            raise InvalidParamError(
                "Veuillez indiquer au moins un paramètre de recherche."
            )
        return self

    @model_validator(mode="after")
    def check_if_short_terms(self):
        """Prevent performance issues by refusing query terms less than 3 characters."""
        if self.terms is not None and len(self.terms) < FIELD_LENGTHS["terms"]:
            raise InvalidParamError(
                "3 caractères minimum pour les termes de la requête"
            )
        return self

    @model_validator(mode="after")
    def total_results_should_be_smaller_than_10000(self):
        if self.page * self.per_page > NUMERIC_FIELD_LIMITS["total_results"]["max"]:
            raise InvalidParamError(
                "Le nombre total de résultats est restreint à 10 000. "
                "Pour garantir cela, le produit du numéro de page "
                "(par défaut, page = 1) et du nombre de résultats par page "
                "(par défaut, per_page = 10), c'est-à-dire `page * per_page`, "
                "ne doit pas excéder 10 000."
            )
        return self
