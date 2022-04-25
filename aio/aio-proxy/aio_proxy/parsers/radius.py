from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer un radius entier ou flottant, en km.")
def parse_and_validate_radius(request):
    radius = float(request.rel_url.query.get("radius", 5))  # default 5
    return radius
