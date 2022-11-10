from typing import Optional


def validate_id_rge(id_rge: str) -> Optional[str]:
    """Check the validity of RGE.

    Args:
        id_rge(str, optional): id RGE

    Returns:
        None if id_rge is None.
        id_rge if valid.

    Raises:
        ValueError: if id_rge not valid.
        Caution: there is no formated way to describe RGE - To verify
    """
    if id_rge is None:
        return None
    return id_rge
