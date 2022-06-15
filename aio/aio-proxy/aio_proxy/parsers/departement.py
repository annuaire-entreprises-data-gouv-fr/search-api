import re
from typing import Optional


def validate_departement(departement_clean: str) -> Optional[str]:
    """Check the validity of departement.

    Args:
        departement_clean(str, optional): departement extracted and cleaned.

    Returns:
        None if departement_clean is None.
        departement_clean if valid.

    Raises:
        ValueError: if departement_clean not valid.
    """
    if departement_clean is None:
        return None
    departements_valides = r"\b([013-8]\d?|2[aAbB1-9]?|9[0-59]?|97[12346])\b"
    if not re.search(departements_valides, departement_clean):
        raise ValueError("Département non valide.")
    return departement_clean
