from typing import List, Optional

from aio_proxy.labels.helpers import codes_naf


def validate_activite_principale(
    list_activite_principale_clean: List[str],
) -> Optional[List[str]]:
    """Check the validity of list_activite_principale.

    Args:
        list_activite_principale_clean(list(str), optional): activite_principale
        extracted and cleaned.

    Returns:
        None if activite_principale_clean is None.
        list_activite_principale_clean if valid.

    Raises:
        ValueError: if one of the values in list_activite_principale_clean is not valid.
    """
    if list_activite_principale_clean is None:
        return None
    for activite_principale in list_activite_principale_clean:
        if len(activite_principale) != 6:
            raise ValueError("Chaque activité principale doit contenir 6 caractères.")
        if activite_principale not in codes_naf:
            raise ValueError("Au moins une des activités principales est inconnue.")
    return list_activite_principale_clean
