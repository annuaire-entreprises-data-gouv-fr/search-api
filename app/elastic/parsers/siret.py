import re


def clean_siret(query_string: str) -> str:
    return query_string.replace(" ", "")


def is_siret(query_string: str) -> bool:
    """
    Check if string is siret (composed of 14 digits).
    """
    if query_string is None or not isinstance(query_string, str):
        return False
    clean_query_string = clean_siret(query_string)
    # Using regular expression to check for exactly 14 digits
    return bool(re.fullmatch(r"^\d{14}$", clean_query_string))
