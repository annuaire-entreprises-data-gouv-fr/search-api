from aio_proxy.decorators.value_exception import value_exception_handler

MIN_RADIUS = 0
MAX_RADIUS = 50


@value_exception_handler(
    error="Veuillez indiquer un radius entier ou flottant entre 0 et 50 (en km)."
)
def parse_and_validate_radius(request):
    """Extract and Check the validity of the radius.

    Args:
        request: HTTP request.

    Returns:
        radius(float) if valid.
        default 5(km).

    Raises:
        ValueError: if page is not float.
    """
    radius = float(request.rel_url.query.get("radius", 5))  # default 5
    if radius <= MIN_RADIUS or radius > MAX_RADIUS:
        raise ValueError
    return radius
