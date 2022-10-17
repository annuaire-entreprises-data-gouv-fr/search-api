from typing import Optional

def validate_finess(finess: str) -> Optional[str]:
    """Check the validity of finess.

    Args:
        finess(str, optional): id FINESS

    Returns:
        None if finess is None.
        finess if valid.

    Raises:
        ValueError: if finess not valid.
    """
    if finess is None:
        return None
    if len(finess) != 9:
        raise ValueError("L'identifiant FINESS doit contenir 9 caractères.")
    return finess
