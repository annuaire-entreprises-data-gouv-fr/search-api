import re

# A numéro RNF identifies a fondation in the Registre national des fonds et fondations
# It is built from the département code, the type of organisme (FDD, FE, FRUP), a sequence number and a check sequence.
# Example: 092-FDD-00061-08
NUMERO_RNF_PATTERN = re.compile(r"\d{3}-[A-Z]{2,4}-\d{5}-\d{2}")


def is_numero_rnf(query_string: str) -> bool:
    """Check if string is a numéro RNF."""
    if query_string is None or not isinstance(query_string, str):
        return False
    return bool(NUMERO_RNF_PATTERN.fullmatch(query_string.strip().upper()))
