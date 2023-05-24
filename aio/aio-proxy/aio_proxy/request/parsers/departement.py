from aio_proxy.labels.helpers import departements


def validate_departement(list_departement_clean: list[str]):
    """Check the validity of list_departement.

    Args:
        list_departement_clean(list(str), optional): list of departements extracted and
        cleaned.

    Returns:
        None if list_departement_clean is None.
        list_departement_clean if valid.

    Raises:
        ValueError: if one of the values of list_departement_clean is not valid.
    """
    if list_departement_clean is None:
        return None
    for departement in list_departement_clean:
        if departement not in departements:
            raise ValueError(
                f"Au moins un département est non valide."
                f" Les départements valides"
                f" : {[dep for dep in departements]}"
            )
    return list_departement_clean
