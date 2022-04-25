from typing import Optional


def validate_is_entrepreneur_individuel(
    is_entrepreneur_individuel_clean: str,
) -> Optional[bool]:
    """Check the validity of is_entrepreneur_individuel.

    Args:
        is_entrepreneur_individuel_clean(str, optional): is_entrepreneur_individuel
                                                        extracted and cleaned.

    Returns:
        None if is_entrepreneur_individuel_clean is None.
        True if is_entrepreneur_individuel_clean==YES.
        False if is_entrepreneur_individuel_clean==NO.

    Raises:
        ValueError: otherwise.
    """
    if is_entrepreneur_individuel_clean is None:
        return None
    if is_entrepreneur_individuel_clean not in ["YES", "NO"]:
        raise ValueError(
            "Seuls les valeurs 'yes' ou bien 'no' sont possibles pour 'is_"
            "entrepreneur_individuel'."
        )
    return is_entrepreneur_individuel_clean == "YES"
