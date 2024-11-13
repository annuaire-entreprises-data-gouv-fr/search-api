SIREN_LENGTH = 9  # Constant for the length of a SIREN number


def is_siren(query_string: str) -> bool:
    """
    Check if string is siren (composed of 9 digits).
    """
    if query_string is None or not isinstance(query_string, str):
        return False
    clean_query_string = query_string.replace(" ", "")
    if len(clean_query_string) != SIREN_LENGTH or not clean_query_string.isdigit():
        return False
    return True
