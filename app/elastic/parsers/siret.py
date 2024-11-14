import re


def is_siret(query_string: str) -> bool:
    """
    Check if string is siret (composed of 14 digits).
    """
    if query_string is None or not isinstance(query_string, str):
        return False
    clean_query_string = query_string.replace(" ", "")
    # Using regular expression to check for exactly 9 digits
    return bool(re.fullmatch(r"^\d{14}$", clean_query_string))
