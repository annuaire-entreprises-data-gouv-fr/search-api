from aio_proxy.labels.helpers import valid_fields


def validate_fields(list_fields_clean: list[str]):
    """Check the validity of list_section_activite_principale.

    Args:
        list_fields_clean(list(str), optional):
        list_fields extracted and cleaned.

    Returns:
        None if list_fields_clean is None.
        list_fields_clean if valid.

    Raises:
        ValueError: if one of the values in list_fields_clean is not valid.
    """
    if list_fields_clean is None:
        return None
    for field in list_fields_clean:
        if field not in valid_fields:
            raise ValueError(
                f"Au moins un champs est non valide. "
                f"Les champs valides : "
                f"{[field for field in valid_fields]}."
            )
    return list_fields_clean
