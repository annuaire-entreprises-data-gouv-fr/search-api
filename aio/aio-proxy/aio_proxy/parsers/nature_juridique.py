from typing import List


def validate_nature_juridique(list_nature_juridique_clean: List[str]):
    """Check the validity of list_section_activite_principale.

    Args:
        list_nature_juridique_clean(list(str), optional):
        list_nature_juridique extracted and cleaned.

    Returns:
        None if list_nature_juridique_clean is None.
        list_nature_juridique_clean if valid.

    Raises:
        ValueError: if one of the values in list_nature_juridique_clean is not valid.
    """
    if list_nature_juridique_clean is None:
        return None
    for nature_juridique in list_nature_juridique_clean:
        if len(nature_juridique) != 4 or not nature_juridique.isdigit():
            raise ValueError("Au moins une nature juridique est non valide.")
    return list_nature_juridique_clean
