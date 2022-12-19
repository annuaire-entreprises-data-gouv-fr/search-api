from typing import Optional


def match_ess_bool_to_value(ess_bool: bool) -> Optional[str]:
    """Match bool filter value to corresponding field value .

    Args:
        ess_bool (str): `est_ess` value extracted from request

    Returns:
        None if `est_ess`is None.
        "O" if `est_ess` is True.
        "N" if `est_ess` is False.

    """
    if ess_bool is None:
        return None
    if ess_bool is True:
        ess = "O"
    else:
        ess = "N"
    return ess
