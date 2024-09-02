import json


def extract_idcc_siret_mapping_from_ul(ul_result):
    """
    Extracts the mapping of SIRET numbers per IDCC from the given Elasticsearch
    result for a SIREN number.

    Args:
        ul_result (dict): Elasticsearch document containing information related to
                          the SIREN.

    Returns:
        dict: A dictionary mapping IDCC codes (str) to lists of SIRET numbers
        (list of str) associated with the given SIREN. Returns an empty dictionary
        if no IDCCs are found or if parsing fails.
    """
    idcc_siret_mapping = ul_result["unite_legale"]["sirets_par_idcc"]

    if idcc_siret_mapping:
        # Replace single quotes with double quotes to form valid JSON
        idcc_siret_mapping_str = idcc_siret_mapping.replace("'", '"')
        return json.loads(idcc_siret_mapping_str)

    return {}
