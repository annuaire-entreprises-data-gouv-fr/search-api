from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(
    error="Veuillez indiquer un numéro de page entier, par défaut 1."
)
def parse_and_validate_page(request) -> int:
    page = int(request.rel_url.query.get("page", 1)) - 1  # default 1
    return page
