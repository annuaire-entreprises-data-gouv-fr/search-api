def validate_id_convention_collective(id_convention_collective: str) -> str | None:
    """Check the validity of id convention collective.

    Args:
        id_convention_collective (str, optional): id convention collective

    Returns:
        None if id_convention_collective is None.
        idcc if valid.

    Raises:
        ValueError: if id_convention_collective not valid.
    """
    if id_convention_collective is None:
        return None
    length_convention_collective = 4
    if len(id_convention_collective) != length_convention_collective:
        raise ValueError(
            "L'identifiant de convention collective doit contenir 4 caractères."
        )
    return id_convention_collective
