from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer une longitude entre -180° et 180°.")
def parse_and_validate_longitude(request):
    lon = float(request.rel_url.query.get("long"))
    if lon > 180 or lon < -180:
        raise ValueError
    return lon
