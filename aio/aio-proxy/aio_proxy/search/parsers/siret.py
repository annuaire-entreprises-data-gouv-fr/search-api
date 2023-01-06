import re


def is_siret(query_string: str) -> bool:
    """
    Check if string is siret (composed of 14 digits).
    """
    if query_string is None:
        return False
    clean_query_string = query_string.replace(" ", "")
    siret_valides = r"\b\d{14}\b"
    if re.search(siret_valides, clean_query_string):
        return True
    return False
