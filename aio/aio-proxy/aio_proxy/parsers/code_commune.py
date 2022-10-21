import re
from typing import Optional


def validate_code_commune(code_commune_clean: str) -> Optional[str]:
    """Check the validity of code_commune.

    Args:
        code_commune_clean(str, optional): code commune extracted and cleaned.

    Returns:
        None if code_commune_clean is None.
        code_commune_clean if valid.

    Raises:
        ValueError: if code_commune_clean not valid.
    """
    if code_commune_clean is None:
        return None
    if len(code_commune_clean) != 5:
        raise ValueError("Code commune doit contenir 5 caractères !")
    codes_valides = r"^(0[1-9]|[1-9][ABab\d])\d{3}$"
    if not re.search(codes_valides, code_commune_clean):
        raise ValueError("Code commune non valide.")
    return code_commune_clean
