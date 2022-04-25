from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer une latitude entre -90° et 90°.")
def parse_and_validate_latitude(request):
    lat = float(request.rel_url.query.get("lat"))
    if lat > 90 or lat < -90:
        raise ValueError
    return lat
