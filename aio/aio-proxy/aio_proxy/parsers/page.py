from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(
    error="Veuillez indiquer un numéro de page entier supérieur ou égal à 1, "
    "par défaut 1."
)
def parse_and_validate_page(request) -> int:
    """Extract and Check the validity of page number.

    Args:
        request: HTTP request.

    Returns:
        page(int) if valid.
        default 1.

    Raises:
        ValueError: if page is not integer.
    """
    page = int(request.rel_url.query.get("page", 1)) - 1  # default 1
    if page <= -1:
        raise ValueError(
            "Veuillez indiquer un numéro de page entier supérieur ou "
            "égal à 1, par défaut 1."
        )
    return page
