from aio_proxy.decorators.value_exception import value_exception_handler
from datetime import date


@value_exception_handler(
    error="Veuillez indiquer une date sous format : aaaa-mm-jj. Exemple : '1990-01-02'"
)
def parse_date(request, param: str, default_value=None):
    """Extract date param from request.

    Args:
        request: HTTP request
        param (str): parameter to extract from request
        default_value:

    Returns:
        None if None.
        param otherwise.
    """
    date = request.rel_url.query.get(param, default_value)
    if date is None:
        return None
    return date.fromisoformat(date)
