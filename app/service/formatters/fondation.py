import json

from app.models.fondation import FondationResponse
from app.utils.helpers import convert_date_to_iso, get_value, is_dev_env


def format_fondation(fondation, meta=None):
    formatted_fondation = FondationResponse(
        numero_rnf=get_value(fondation, "numero_rnf"),
        denomination=get_value(fondation, "denomination"),
        type_organisme=get_value(fondation, "type_organisme"),
        date_creation=convert_date_to_iso(get_value(fondation, "date_creation")),
        adresse=get_value(fondation, "adresse"),
        code_postal=get_value(fondation, "code_postal"),
        ville=get_value(fondation, "ville"),
        siren=get_value(fondation, "siren"),
        siret=get_value(fondation, "siret"),
    )

    if meta and is_dev_env():
        formatted_fondation.score = meta.get("score")
        formatted_fondation.meta = json.loads(json.dumps(meta, default=str))

    return formatted_fondation.dict(exclude_unset=True)


def format_fondation_results(results, search_params):
    """Main formatting function for all fondations results."""
    formatted_results = []

    for search_result in results:
        # If structure is fondation
        if "fondation" in search_result:
            formatted_results.append(
                format_fondation(search_result["fondation"], search_result.get("meta"))
            )

    return formatted_results
