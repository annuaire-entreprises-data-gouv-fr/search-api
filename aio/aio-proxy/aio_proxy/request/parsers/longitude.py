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
    min_longitude = -180
    max_longitude = 180
    lon_str = request.rel_url.query.get("long")
    if lon_str == "nan":
        raise ValueError
    try:
        lon = float(lon_str)
    except ValueError:
        raise ValueError
    if lon > max_longitude or lon < min_longitude:
        raise ValueError
    return lon
