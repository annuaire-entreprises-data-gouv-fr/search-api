from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(
    error="Veuillez indiquer un nombre d'établissements connexes entier entre 1 et "
    "100, par défaut 10."
)
def parse_and_validate_matching_size(request) -> int:
    """Extract and Check the validity of page number.

    Args:
        request: HTTP request.

    Returns:
        matching_size(int) if valid.
        default 10.

    Raises:
        ValueError: if matching_size is not integer.
    """
    matching_size = int(request.rel_url.query.get("limite_matching_etablissements", 10))
    min_matching_size = 0
    max_matching_size = 100
    if matching_size <= min_matching_size or matching_size > max_matching_size:
        raise ValueError(
            "Veuillez indiquer un nombre d'établissements connexes entier entre 1 et "
            "100, par défaut 10."
        )
    return matching_size
