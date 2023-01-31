from typing import List, Optional

from aio_proxy.labels.helpers import sections_codes_naf


def validate_section_activite_principale(
    list_section_activite_principale_clean: List[str],
) -> Optional[List[str]]:
    """Check the validity of list_section_activite_principale.

    Args:
        list_section_activite_principale_clean(list(str), optional):
        list_section_activite_principale extracted and cleaned.

    Returns:
        None if list_section_activite_principale_clean is None.
        list_section_activite_principale_clean if valid.

    Raises:
        ValueError: if one on the values in list_section_activite_principale_clean
        is not valid.
    """
    if list_section_activite_principale_clean is None:
        return None
    for section_activite_principale in list_section_activite_principale_clean:
        if section_activite_principale not in sections_codes_naf:
            raise ValueError(
                "Au moins une section d'activité principale est non valide."
            )
    return list_section_activite_principale_clean
