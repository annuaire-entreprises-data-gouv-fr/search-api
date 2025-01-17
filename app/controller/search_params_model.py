import re
from datetime import date

from pydantic import BaseModel, field_validator, model_validator

from app.controller.field_validation import (
    FIELD_LENGTHS,
    NUMERIC_FIELD_LIMITS,
    VALID_ADMIN_FIELDS_TO_SELECT,
    VALID_FIELD_VALUES,
    VALID_FIELDS_TO_SELECT,
)
from app.exceptions.exceptions import (
    InvalidParamError,
)
from app.service.search_type import SearchType
from app.utils.helpers import (
    check_params_are_none_except_excluded,
    clean_str,
    match_bool_to_insee_value,
    str_to_list,
)


class SearchParams(BaseModel):
    """Class for modeling search parameters"""

    search_type: SearchType
    page: int = 1
    page_etablissements: int | None = None
    per_page: int = 10
    terms: str | None = None
    activite_principale_unite_legale: list | None = None
    categorie_entreprise: list | None = None
    commune: list | None = None
    code_postal: list | None = None
    departement: list | None = None
    region: list | None = None
    est_entrepreneur_individuel: bool | None = None
    section_activite_principale: list | None = None
    tranche_effectif_salarie_unite_legale: list | None = None
    convention_collective_renseignee: bool | None = None
    egapro_renseignee: bool | None = None
    epci: list | None = None
    est_bio: bool | None = None
    est_finess: bool | None = None
    est_uai: bool | None = None
    est_collectivite_territoriale: bool | None = None
    est_entrepreneur_spectacle: bool | None = None
    est_association: bool | None = None
    est_ess: bool | None = None
    est_organisme_formation: bool | None = None
    est_qualiopi: bool | None = None
    est_rge: bool | None = None
    est_service_public: bool | None = None
    est_societe_mission: bool | None = None
    id_convention_collective: str | None = None
    id_finess: str | None = None
    id_uai: str | None = None
    code_collectivite_territoriale: list | None = None
    id_rge: str | None = None
    nom_personne: str | None = None
    prenoms_personne: str | None = None
    min_date_naiss_personne: date | None = None
    max_date_naiss_personne: date | None = None
    ca_min: int | None = None
    ca_max: int | None = None
    resultat_net_min: int | None = None
    resultat_net_max: int | None = None
    type_personne: str | None = None
    etat_administratif_unite_legale: str | None = None
    nature_juridique_unite_legale: list | None = None
    est_siae: bool | None = None
    matching_size: int = 10
    lat: float | None = None
    lon: float | None = None
    radius: float | None = 5
    minimal: bool | None = False
    include: list | None = None
    include_admin: list | None = None
    sort_by_size: bool | None = None

    # Field Validators (involve one field at a time)
    @field_validator(
        "page", "page_etablissements", "per_page", "matching_size", mode="before"
    )
    def cast_as_integer(cls, value: str, info) -> int:
        try:
            int(value)
        except ValueError:
            raise InvalidParamError(
                f"Veuillez indiquer un paramètre `{info.field_name}` entier."
            )
        return int(value)

    @field_validator("radius", "lat", "lon", mode="before")
    def cast_as_float(cls, value: str, info) -> float:
        try:
            if value.lower() == "nan":
                raise ValueError
            float(value)
        except ValueError:
            raise InvalidParamError(
                f"Veuillez indiquer un paramètre `{info.field_name}` flottant."
            )
        return float(value)

    @field_validator(
        "page",
        "page_etablissements",
        "per_page",
        "matching_size",
        "radius",
        "lat",
        "lon",
        mode="after",
    )
    # Apply after first validator and Pydantic internal validation
    def check_if_number_in_range(cls, value, info):
        limits = NUMERIC_FIELD_LIMITS.get(info.field_name)
        if value < limits.get("min") or value > limits.get("max"):
            raise InvalidParamError(
                f"Veuillez indiquer un paramètre `{info.field_name}` entre "
                f"`{limits.get('min')}` et `{limits.get('max')}`, "
                f"par défaut `{limits['default']}`."
            )
        return value

    @field_validator(
        "terms",
        "type_personne",
        "etat_administratif_unite_legale",
        mode="before",
    )
    def make_uppercase(cls, value: str) -> str:
        return value.upper()

    @field_validator(
        "nature_juridique_unite_legale",
        "categorie_entreprise",
        "departement",
        "tranche_effectif_salarie_unite_legale",
        "section_activite_principale",
        "region",
        "activite_principale_unite_legale",
        "code_collectivite_territoriale",
        "commune",
        "epci",
        "code_postal",
        "include",
        "include_admin",
        mode="before",
    )
    def convert_str_to_list(cls, str_of_values: str) -> list[str]:
        list_of_values = str_to_list(clean_str(str_of_values))
        return list_of_values

    @field_validator("code_postal", "commune", "epci", mode="after")
    def list_of_values_should_match_regular_expression(
        cls, list_values: list[str], info
    ) -> list[str]:
        for value in list_values:
            valid_values = VALID_FIELD_VALUES.get(info.field_name)["valid_values"]
            if not re.search(valid_values, value):
                raise InvalidParamError(
                    f"Au moins une valeur du paramètre {info.field_name} "
                    "est non valide."
                )
        return list_values

    @field_validator(
        "nature_juridique_unite_legale",
        "categorie_entreprise",
        "departement",
        "tranche_effectif_salarie_unite_legale",
        "section_activite_principale",
        "region",
        "activite_principale_unite_legale",
        mode="after",
    )
    def list_of_values_must_be_valid(cls, list_of_values: list[str], info) -> list[str]:
        valid_values = VALID_FIELD_VALUES.get(info.field_name)["valid_values"]
        for value in list_of_values:
            if value not in valid_values:
                raise InvalidParamError(
                    f"Au moins un paramètre "
                    f"`{VALID_FIELD_VALUES.get(info.field_name)['alias']}` "
                    f"est non valide. "
                    f"Les valeurs valides : {[value for value in valid_values]}."
                )
        return list_of_values

    @field_validator("type_personne", "etat_administratif_unite_legale", mode="after")
    def field_must_be_in_valid_list(cls, value: str, info) -> str:
        valid_values = VALID_FIELD_VALUES.get(info.field_name)["valid_values"]
        if value not in valid_values:
            raise InvalidParamError(
                f"Le paramètre `{VALID_FIELD_VALUES.get(info.field_name)['alias']}` "
                f"doit prendre une des valeurs suivantes {valid_values}."
            )
        return value

    @field_validator(
        "est_entrepreneur_individuel",
        "convention_collective_renseignee",
        "egapro_renseignee",
        "est_bio",
        "est_finess",
        "est_uai",
        "est_collectivite_territoriale",
        "est_entrepreneur_spectacle",
        "est_ess",
        "est_association",
        "est_organisme_formation",
        "est_qualiopi",
        "est_rge",
        "est_service_public",
        "minimal",
        "est_societe_mission",
        "est_siae",
        "sort_by_size",
        mode="before",
    )
    def convert_str_to_bool(cls, boolean: str, info) -> bool:
        param_name = info.field_name
        if boolean.upper() not in ["TRUE", "FALSE"]:
            raise InvalidParamError(
                f"{param_name} doit prendre la valeur 'true' ou 'false' !"
            )
        return boolean.upper() == "TRUE"

    @model_validator(mode="after")
    def validate_search_type_params(self):
        """Validate parameters based on search type"""
        if self.search_type == SearchType.GEO:
            # For geo search, require lat/lon and don't allow terms
            if self.terms is not None:
                raise InvalidParamError(
                    "Le paramètre 'terms' n'est pas autorisé pour une recherche "
                    "géographique."
                )
            if self.lat is None or self.lon is None:
                raise InvalidParamError(
                    "Les paramètres 'lat' et 'long' sont obligatoires pour une "
                    "recherche géographique."
                )

        elif self.search_type == SearchType.TEXT:
            # For text search, don't allow lat/lon
            if any([self.lat is not None, self.lon is not None]):
                raise InvalidParamError(
                    "Les paramètres 'lat', 'long' ne sont autorisés "
                    "que pour une recherche géographique."
                )
        return self

    @field_validator("est_societe_mission", mode="after")
    def convert_bool_to_insee_value(cls, boolean: bool) -> str:
        return match_bool_to_insee_value(boolean)

    @field_validator("id_convention_collective", "id_finess", "id_uai", mode="before")
    def check_str_length(cls, field_value: str, info) -> str:
        field_length = FIELD_LENGTHS.get(info.field_name)
        if len(field_value) != field_length:
            raise InvalidParamError(
                f"Le paramètre `{info.field_name}` "
                f"doit contenir {field_length} caractères."
            )
        return field_value

    @field_validator("code_collectivite_territoriale", mode="after")
    def check_min_str_length_in_list(cls, list_values: list[str], info) -> list[str]:
        min_value_len = FIELD_LENGTHS.get(info.field_name)
        for value in list_values:
            if len(value) < min_value_len:
                raise InvalidParamError(
                    """Chaque identifiant code insee d'une collectivité
                    territoriale doit contenir au moins 2 caractères."""
                )
        return list_values

    @field_validator("nom_personne", "prenoms_personne", mode="before")
    def clean_name(cls, value: str) -> str:
        return value.replace("-", " ").lower()

    @field_validator(
        "min_date_naiss_personne", "max_date_naiss_personne", mode="before"
    )
    def check_date_format(cls, date_string: str) -> date:
        try:
            return date.fromisoformat(date_string)
        except Exception:
            raise InvalidParamError(
                "Veuillez indiquer une date sous "
                "le format : aaaa-mm-jj. Exemple : '1990-01-02'"
            )

    @field_validator("include", "include_admin", mode="after")
    def validate_include(cls, list_fields: list[str], info) -> list[str]:
        if info.field_name == "include_admin":
            valid_fields_to_check = VALID_ADMIN_FIELDS_TO_SELECT
        else:
            valid_fields_to_check = VALID_FIELDS_TO_SELECT
        for field in list_fields:
            if field not in valid_fields_to_check:
                valid_fields_lowercase = [
                    field.lower() for field in valid_fields_to_check
                ]
                raise InvalidParamError(
                    "Au moins un champ à inclure est non valide. "
                    f"Les champs valides : {valid_fields_lowercase}."
                )
        return list_fields

    # Model Validators (involve more than one field at a time)
    @model_validator(mode="after")
    def total_results_should_be_smaller_than_10000(self):
        page = self.page
        per_page = self.per_page
        if page * per_page > NUMERIC_FIELD_LIMITS["total_results"]["max"]:
            raise InvalidParamError(
                "Le nombre total de résultats est restreint à 10 000. "
                "Pour garantir cela, le produit du numéro de page "
                "(par défaut, page = 1) et du nombre de résultats par page "
                "(par défaut, per_page = 10), c'est-à-dire `page * per_page`, "
                "ne doit pas excéder 10 000."
            )
        return self

    @model_validator(mode="after")
    def validate_date_range(self):
        min_date_naiss = self.min_date_naiss_personne
        max_date_naiss = self.max_date_naiss_personne
        if min_date_naiss and max_date_naiss:
            if max_date_naiss < min_date_naiss:
                raise InvalidParamError(
                    "Veuillez indiquer une date minimale inférieure à la date maximale."
                )
        return self

    @model_validator(mode="after")
    def validate_inclusion_fields(self):
        include = self.include
        minimal = self.minimal
        if include and (minimal is None or minimal is False):
            raise InvalidParamError(
                "Veuillez indiquer si vous souhaitez une réponse minimale "
                "avec le filtre `minimal=True`` avant de préciser les "
                "champs à inclure."
            )
        return self

    @model_validator(mode="after")
    def check_if_all_empty_params(self):
        """
        If all parameters are empty (except matching size and pagination
        because they always have a default value) raise value error
        Check if all non-default parameters are empty, raise a InvalidParamError
        if they are
        """
        excluded_fields = [
            "search_type",
            "radius",
            "page",
            "page_etablissements",
            "per_page",
            "matching_size",
            "minimal",
            "include",
            "include_admin",
            "sort_by_size",
        ]

        all_fields_are_null_except_excluded = check_params_are_none_except_excluded(
            self.dict(exclude_unset=True), excluded_fields
        )
        if all_fields_are_null_except_excluded:
            raise InvalidParamError(
                "Veuillez indiquer au moins un paramètre de recherche."
            )
        return self

    @model_validator(mode="after")
    def check_if_short_terms_and_no_other_param(self):
        """Prevent performance issues by refusing query terms less than 3 characters.
        Accept less than 3 characters if at least one parameter is filled.
        Except matching size, because this param always has a default value.
        """
        # List of parameters to exclude from the check
        excluded_fields = [
            "search_type",
            "radius",
            "page",
            "per_page",
            "matching_size",
            "terms",
            "minimal",
            "include",
            "include_admin",
            "sort_by_size",
        ]

        all_fields_are_null_except_excluded = check_params_are_none_except_excluded(
            self.dict(exclude_unset=True), excluded_fields
        )
        if (
            self.terms is not None
            and len(self.terms) < FIELD_LENGTHS["terms"]
            and all_fields_are_null_except_excluded
        ):
            raise InvalidParamError(
                "3 caractères minimum pour les termes de la requête "
                + "(ou utilisez au moins un filtre)"
            )
        return self
