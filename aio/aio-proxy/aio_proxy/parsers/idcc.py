from typing import Optional

def validate_idcc(idcc: str) -> Optional[str]:
    """Check the validity of idcc.

    Args:
        idcc(str, optional): id convention collective

    Returns:
        None if idcc is None.
        idcc if valid.

    Raises:
        ValueError: if idcc not valid.
    """
    if idcc is None:
        return None
    if len(idcc) != 4:
        raise ValueError("L'identifiant de convention collective doit contenir 4 caractères.")
    return idcc
