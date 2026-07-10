from app.controller.fondation_params_model import FondationParams


class FondationParamsBuilder:
    """Class for building and modeling the fondation search parameters"""

    # Some field names in API do not exactly match their variable name in Elasticsearch
    PARAMETER_MAPPING = {"q": "terms"}

    @staticmethod
    def extract_params(request):
        """Map the request parameters to match the Pydantic model's field name."""
        mapped_params = {}
        for param, param_value in request.query_params.items():
            # Include parameters not specified in PARAMETER_MAPPING without mapping
            mapped_field = FondationParamsBuilder.PARAMETER_MAPPING.get(param, param)
            mapped_params[mapped_field] = param_value
        return FondationParams(**mapped_params)
