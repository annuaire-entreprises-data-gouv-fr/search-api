def validate_id_uai(id_uai: str) -> str | None:
    """Check the validity of id_uai.

    Args:
        id_uai(str, optional): id UAI

    Returns:
        None if id_uai is None.
        id_uai if valid.

    Raises:
        ValueError: if id_uai not valid.
    """
    if id_uai is None:
        return None
    length_id_uai = 8
    if len(id_uai) != length_id_uai:
        raise ValueError("L'identifiant UAI doit contenir 8 caractères.")
    return id_uai
