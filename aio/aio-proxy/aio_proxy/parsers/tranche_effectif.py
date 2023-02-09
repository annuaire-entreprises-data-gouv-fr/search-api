from aio_proxy.labels.helpers import tranches_effectifs


def validate_tranche_effectif_salarie(
    list_tranche_effectif_salarie_clean: list[str],
) -> list[str] | None:
    """Check the validity of list_tranche_effectif_salarie.

    Args:
        list_tranche_effectif_salarie_clean(list(str), optional):
        list_tranche_effectif_salarie extracted and cleaned.

    Returns:
        None if list_tranche_effectif_salarie_clean is None.
        list_tranche_effectif_salarie_clean if valid.

    Raises:
        ValueError: if one value in list_tranche_effectif_salarie_clean is not valid.
    """
    if list_tranche_effectif_salarie_clean is None:
        return None
    length_tranche_effectif_salarie = 2
    for tranche_effectif_salarie in list_tranche_effectif_salarie_clean:
        if len(tranche_effectif_salarie) != length_tranche_effectif_salarie:
            raise ValueError("Chaque tranche salariés doit contenir 2 caractères.")
        if tranche_effectif_salarie not in tranches_effectifs:
            raise ValueError("Au moins une tranche salariés est non valide.")
    return list_tranche_effectif_salarie_clean
