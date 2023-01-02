import re
from typing import List, Optional


def validate_departement(list_departement_clean: List[str]) -> Optional[List[str]]:
    """Check the validity of list_departement.

    Args:
        list_departement_clean(list(str), optional): list of departements extracted and
        cleaned.

    Returns:
        None if lit_departement_clean is None.
        list_departement_clean if valid.

    Raises:
        ValueError: if one of the values of list_departement_clean is not valid.
    """
    if list_departement_clean is None:
        return None
    for departement in list_departement_clean:
        departements_valides = r"\b([013-8]\d?|2[aAbB1-9]?|9[0-59]?|97[12346])\b"
        if not re.search(departements_valides, departement):
            raise ValueError("Au moins un département est non valide.")
    return list_departement_clean
