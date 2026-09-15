import re


def clean_siren(query_string: str) -> str:
    return query_string.replace(" ", "")


def is_siren(query_string: str) -> bool:
    """
    Check if string is siren (composed of exactly 9 digits).
    """

    if query_string is None or not isinstance(query_string, str):
        return False
    clean_query_string = clean_siren(query_string)
    # Using regular expression to check for exactly 9 digits
    return bool(re.fullmatch(r"^\d{9}$", clean_query_string))
