from typing import Optional

from aio_proxy.labels.helpers import codes_naf


def validate_activite_principale(activite_principale_clean: str) -> Optional[str]:
    """Check the validity of activite_principale.

    Args:
        activite_principale_clean(str, optional): activite_principale extracted and
                                                cleaned.

    Returns:
        None if activite_principale_clean is None.
        activite_principale_clean if valid.

    Raises:
        ValueError: if activite_principale_clean not valid.
    """
    if activite_principale_clean is None:
        return None
    if len(activite_principale_clean) != 6:
        raise ValueError("Activité principale doit contenir 6 caractères.")
    if activite_principale_clean not in codes_naf:
        raise ValueError("Activité principale inconnue.")
    return activite_principale_clean
