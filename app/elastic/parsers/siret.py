SIRET_LENGTH = 14  # Constant for the length of a SIRET number


def is_siret(query_string: str) -> bool:
    """
    Check if string is siret (composed of 14 digits).
    """
    if query_string is None or not isinstance(query_string, str):
        return False

    clean_query_string = query_string.replace(" ", "")

    # Validate length and digit-only condition
    if len(clean_query_string) == SIRET_LENGTH and clean_query_string.isdigit():
        return True

    return False
