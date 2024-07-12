import json


def extract_list_idcc_by_siren_from_ul(ul_result):
    """
    Extracts the list of IDCCs from the given Elasticsearch result for a SIREN.

    Args:
        ul_result (dict): Elasticsearch document containing information related to
        the SIREN.

    Returns:
        list: List of IDCCs associated with the SIREN, or an empty list if no IDCCs
        found or if parsing fails.
    """
    idcc_list_json = ul_result["unite_legale"]["liste_idcc_by_siren"]

    if idcc_list_json:
        idcc_list_str = idcc_list_json.replace("'", '"')
        return json.loads(idcc_list_str)

    return []
