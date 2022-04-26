from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer un `per_page` entier, par défaut 10.")
def parse_and_validate_per_page(request) -> int:
    per_page = int(request.rel_url.query.get("per_page", 10))  # default 10
    return per_page