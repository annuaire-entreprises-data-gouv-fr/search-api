from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer une longitude entre -180° et 180°.")
def parse_and_validate_longitude(request):
    """Extract and Check the validity of longitude.

    Args:
        request: HTTP request.

    Returns:
        longitude(float) if valid.

    Raises:
        ValueError: if longitude is not float, or outside range [-180, 180].
    """
    lon = float(request.rel_url.query.get("long"))
    if lon > 180 or lon < -180:
        raise ValueError
    return lon
