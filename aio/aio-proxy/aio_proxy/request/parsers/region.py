from aio_proxy.labels.helpers import regions


def validate_region(list_region_clean: list[str]):
    """Check the validity of list_region.

    Args:
        list_region_clean(list(str), optional): list of regions extracted and
        cleaned.

    Returns:
        None if list_region_clean is None.
        list_region_clean if valid.

    Raises:
        ValueError: if one of the values of list_region_clean is not valid.
    """
    if list_region_clean is None:
        return None
    for region in list_region_clean:
        if region not in regions:
            raise ValueError(
                f"Au moins une region est non valide."
                f" Les région valides"
                f" : {regions}"
            )
    return list_region_clean
