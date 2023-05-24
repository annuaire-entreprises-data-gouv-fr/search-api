from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer une latitude entre -90° et 90°.")
def parse_and_validate_latitude(request):
    """Extract and Check the validity of latitude.

    Args:
        request: HTTP request.

    Returns:
        latitude(float) if valid.

    Raises:
        ValueError: if latitude is not float, or outside range [-90, 90].
    """
    min_latitude = -90
    max_latitude = 90
    lat = float(request.rel_url.query.get("lat"))
    if lat > max_latitude or lat < min_latitude:
        raise ValueError
    return lat
