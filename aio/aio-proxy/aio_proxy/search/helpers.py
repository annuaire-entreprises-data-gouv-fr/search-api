import json
import logging
import os
import re
from typing import Tuple
from urllib.request import urlopen

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_current_color(color_url):
    """Get current Elasticsearch index color from json file stored in MinIO."""
    try:
        with urlopen(color_url, timeout=5) as url:
            data = json.loads(url.read().decode())
            current_color = data["CURRENT_COLOR"]
            logging.info(
                f"******************** Current color from file: {current_color}"
            )
    except BaseException as error:
        logging.info(
            f"******************** Error getting file from MINIO:"
            f"{error}, using: blue as default!!!"
        )
        current_color = "blue"
    return current_color


CURRENT_COLOR = get_current_color(os.getenv("COLOR_URL"))


def is_siren(query_string: str) -> bool:
    """
    Check if string is siren (composed of 9 digits).
    """
    if query_string is None:
        return False
    clean_query_string = query_string.replace(" ", "").upper()
    siren_valides = r"\b\d{9}\b"
    if re.search(siren_valides, clean_query_string):
        return True
    return False


def sort_and_execute_search(
    search,
    offset: int,
    page_size: int,
    is_search_fields,
) -> Tuple:
    search = search.extra(track_scores=True)
    # Sorting is very heavy on performance if there is no
    # search terms (only filters). As there is no search terms, we can
    # exclude this sorting because score is the same for all results
    # documents. Beware, nom and prenoms are search fields.
    if is_search_fields:
        search = search.sort(
            {"_score": {"order": "desc"}},
            {"etat_administratif_siege": {"order": "asc"}},
        )

    search = search[offset : (offset + page_size)]
    results = search.execute()
    total_results = results.hits.total.value
    response = []
    for matched_company in results.hits:
        matched_company_dict = matched_company.to_dict(
            skip_empty=False, include_meta=False
        )
        # Add meta field to response to retrieve score
        matched_company_dict["meta"] = matched_company.meta.to_dict()
        response.append(matched_company_dict)
    return total_results, response


def hide_fields(search_result: list) -> list:
    """Hide concatenation fields in search results."""
    hidden_fields = {
        "coordonnees",
        "concat_nom_adr_siren",
        "concat_enseigne_adresse",
        "geo_adresse",
        "is_siege",
        "liste_adresses",
        "liste_enseignes",
    }
    results = [
        {field: value for field, value in unite.items() if field not in hidden_fields}
        for unite in search_result
    ]
    return results


def get_es_field(param_name):
    if param_name == "est_finess":
        return "liste_finess"
    elif param_name == "id_finess":
        return "liste_finess"
    elif param_name == "est_uai":
        return "liste_uai"
    elif param_name == "id_uai":
        return "liste_uai"
    elif param_name == "est_collectivite_territoriale":
        return "colter_code"
    elif param_name == "code_collectivite_territoriale":
        return "colter_code"
    elif param_name == "est_entrepreneur_spectacle":
        return "is_entrepreneur_spectacle"
    elif param_name == "est_rge":
        return "liste_rge"
    elif param_name == "id_rge":
        return "liste_rge"
    elif param_name == "convention_collective_renseignee":
        return "liste_idcc"
    elif param_name == "id_convention_collective":
        return "liste_idcc"
    else:
        return param_name
