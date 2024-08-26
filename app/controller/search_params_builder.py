from app.controller.search_params_model import SearchParams
from app.request.search_type import SearchType


class SearchParamsBuilder:
    """This class extracts parameter values from request and saves them in a
    SearchParams dataclass object."""

    # Some field names in API do not exactly match their variable name in Elasticsearch
    PARAMETER_MAPPING = {
        "q": "terms",
        "limite_matching_etablissements": "matching_size",
        "nature_juridique": "nature_juridique_unite_legale",
        "date_naissance_personne_min": "min_date_naiss_personne",
        "date_naissance_personne_max": "max_date_naiss_personne",
        "etat_administratif": "etat_administratif_unite_legale",
        "activite_principale": "activite_principale_unite_legale",
        "code_commune": "commune",
        "tranche_effectif_salarie": "tranche_effectif_salarie_unite_legale",
        "long": "lon",
    }

    @staticmethod
    def map_request_parameters(request):
        # Extract all query parameters from the request
        request_params = request.query_params
        mapped_params = {}
        for param, param_value in request_params.items():
            field_should_be_mapped = param in SearchParamsBuilder.PARAMETER_MAPPING
            # Include parameters specified in PARAMETER_MAPPING with mapping
            if field_should_be_mapped:
                mapped_field = SearchParamsBuilder.PARAMETER_MAPPING[param]
                mapped_params[mapped_field] = param_value
            # Include parameters not specified in PARAMETER_MAPPING without mapping
            else:
                mapped_params[param] = param_value
        return mapped_params

    @staticmethod
    def get_search_params(request):
        """Map the request parameters to match the Pydantic model's field name."""
        mapped_params = SearchParamsBuilder.map_request_parameters(request)
        params = SearchParams(**mapped_params)
        return params

    @staticmethod
    def extract_params(request, search_type):
        if search_type in (SearchType.TEXT, SearchType.GEO):
            return SearchParamsBuilder.get_search_params(request)
        else:
            raise ValueError("Unknown search type!!!")
