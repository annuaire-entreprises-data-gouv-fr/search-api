from aio_proxy.decorators.value_exception import value_exception_handler


@value_exception_handler(error="Veuillez indiquer un entier. Exemple : 100000")
def parse_and_validate_int(request, param: str, default_value=None):
    """Extract int param from request.

    Args:
        request: HTTP request
        param (str): parameter to extract from request
        default_value:

    Returns:
        None if None.
        param otherwise.
    """
    int_val = request.rel_url.query.get(param, default_value)
    if int_val is None:
        return None
    return int(int_val)
