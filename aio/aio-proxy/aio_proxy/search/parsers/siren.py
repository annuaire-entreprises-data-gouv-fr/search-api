import re


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
