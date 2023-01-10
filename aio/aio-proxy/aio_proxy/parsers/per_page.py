from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(
    error="Veuillez indiquer un `per_page` entre 1 et 25, par défaut 10."
)
def parse_and_validate_per_page(request) -> int:
    """Extract and Check the validity of per page.

    Args:
        request: HTTP request.

    Returns:
        per_page(int) if valid.
        default 10.

    Raises:
        ValueError: if per_page is not integer.
    """
    per_page = int(request.rel_url.query.get("per_page", 10))  # default 10
    # Limit number of results per page for performance reasons
    if per_page > 25:
        raise ValueError
    return per_page
