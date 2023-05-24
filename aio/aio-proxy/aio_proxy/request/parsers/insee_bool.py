def match_bool_to_insee_value(bool_value: bool) -> str | None:
    """Match bool filter value to corresponding INSEE field value .

    Args:
        bool_value (str): `est_var` value extracted from request

    Returns:
        None if `est_var`is None.
        "O" if `est_var` is True.
        "N" if `est_var` is False.

    """
    if bool_value is None:
        return None
    if bool_value is True:
        insee_value = "O"
    else:
        insee_value = "N"
    return insee_value
