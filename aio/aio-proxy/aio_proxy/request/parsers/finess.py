def validate_id_finess(id_finess: str) -> str | None:
    """Check the validity of finess.

    Args:
        id_finess(str, optional): id FINESS

    Returns:
        None if id_finess is None.
        id_finess if valid.

    Raises:
        ValueError: if id_finess not valid.
    """
    if id_finess is None:
        return None
    len_id_finess = 9
    if len(id_finess) != len_id_finess:
        raise ValueError("L'identifiant FINESS doit contenir 9 caractères.")
    return id_finess
