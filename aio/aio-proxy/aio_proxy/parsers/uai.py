from typing import Optional


def validate_uai(uai: str) -> Optional[str]:
    """Check the validity of uai.

    Args:
        uai(str, optional): id UAI

    Returns:
        None if uai is None.
        uai if valid.

    Raises:
        ValueError: if uai not valid.
    """
    if uai is None:
        return None
    if len(uai) != 8:
        raise ValueError("L'identifiant UAI doit contenir 8 caractères.")
    return uai
