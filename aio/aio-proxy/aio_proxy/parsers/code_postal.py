import re
from typing import Optional


def validate_code_postal(code_postal_clean: str) -> Optional[str]:
    """Check the validity of code_postal.

    Args:
        code_postal_clean(str, optional): code postal extracted and cleaned.

    Returns:
        None if code_postal_clean is None.
        code_postal_clean if valid.

    Raises:
        ValueError: if code_postal_clean not valid.
    """
    if code_postal_clean is None:
        return None
    if len(code_postal_clean) != 5:
        raise ValueError("Code postal doit contenir 5 caractères !")
    codes_valides = "^((0[1-9])|([1-8][0-9])|(9[0-8])|(2A)|(2B))[0-9]{3}$"
    if not re.search(codes_valides, code_postal_clean):
        raise ValueError("Code postal non valide.")
    return code_postal_clean
