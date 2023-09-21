from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(
    error="Veuillez indiquer un `per_page` entre 1 et 25, par défaut 10."
)
def parse_and_validate_per_page(request) -> int:
    per_page = int(request.rel_url.query.get("per_page", 10))  # default 10
    # Limit number of results per page for performance reasons
    max_per_page = 25
    min_per_page = 1
    if per_page > max_per_page or per_page < min_per_page:
        raise ValueError
    return per_page
