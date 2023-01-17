import re
from typing import List


def validate_code_commune(list_code_commune_clean: List[str]):
    """Check the validity of list_code_commune.

    Args:
        list_code_commune_clean(list(str), optional): list of codes commune extracted
        and cleaned.

    Returns:
        None if code_commune_clean is None.
        list_code_commune_clean if valid.

    Raises:
        ValueError: if one of the values in list_code_commune_clean is not valid.
    """
    if list_code_commune_clean is None:
        return None
    for code_commune in list_code_commune_clean:
        if len(code_commune) != 5:
            raise ValueError("Chaque code commune doit contenir 5 caractères !")
        codes_valides = r"^([013-9]\d|2[AB1-9])\d{3}$"
        if not re.search(codes_valides, code_commune):
            raise ValueError("Au moins un des codes communes est non valide.")
    return list_code_commune_clean
