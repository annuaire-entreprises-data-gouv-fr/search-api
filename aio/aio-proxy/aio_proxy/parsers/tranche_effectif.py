from typing import Optional

from aio_proxy.labels.helpers import tranches_effectifs


def validate_tranche_effectif_salarie(
    tranche_effectif_salarie_clean: str,
) -> Optional[str]:
    """Check the validity of tranche_effectif_salarie.

    Args:
        tranche_effectif_salarie_clean(str, optional):
         tranche_effectif_salarie extracted and cleaned.

    Returns:
        None if tranche_effectif_salarie_clean is None.
        tranche_effectif_salarie_clean if valid.

    Raises:
        ValueError: if tranche_effectif_salarie_clean not valid.
    """
    if tranche_effectif_salarie_clean is None:
        return None
    if len(tranche_effectif_salarie_clean) != 2:
        raise ValueError("Tranche salariés doit contenir 2 caractères.")
    if tranche_effectif_salarie_clean not in tranches_effectifs:
        raise ValueError("Tranche salariés non valide.")
    return tranche_effectif_salarie_clean
