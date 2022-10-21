from typing import Optional

from aio_proxy.labels.helpers import sections_codes_naf


def validate_section_activite_principale(
    section_activite_principale_clean: str,
) -> Optional[str]:
    """Check the validity of section_activite_principale.

    Args:
        section_activite_principale_clean(str, optional):
        section_activite_principale extracted and cleaned.

    Returns:
        None if section_activite_principale_clean is None.
        section_activite_principale_clean if valid.

    Raises:
        ValueError: if section_activite_principale_clean not valid.
    """
    if section_activite_principale_clean is None:
        return None
    if section_activite_principale_clean not in sections_codes_naf:
        raise ValueError("Section d'activité principale non valide.")
    return section_activite_principale_clean
