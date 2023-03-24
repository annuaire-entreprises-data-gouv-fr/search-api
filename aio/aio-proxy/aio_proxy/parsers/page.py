from aio_proxy.decorators.value_exception import value_exception_handler

MAX_PAGE_VALUE = 1000
MIN_PAGE_NUMBER = 0


@value_exception_handler(
    error="Veuillez indiquer un numéro de page entier entre 1 et 1000, par défaut 1."
)
def parse_and_validate_page(request) -> int:
    """Extract and Check the validity of page number.

    Args:
        request: HTTP request.

    Returns:
        page(int) if valid.
        default 1.

    Raises:
        ValueError: if page is not integer, lower than 1 or higher than 1000.
    """
    page = int(request.rel_url.query.get("page", 1)) - 1  # default 1
    # 1000 is elasticsearch's default page limit
    if page <= MIN_PAGE_NUMBER - 1 or page >= MAX_PAGE_VALUE:
        raise ValueError
    return page
