from aio_proxy.decorators.value_exception import value_exception_handler

"""
@value_exception_handler(
    error="Veuillez indiquer la requête avec le paramètre: ?q=ma+recherche."
)
"""


def parse_and_validate_terms(request, default_value=None):
    """Extract search terms from request.

    Args:
        request: HTTP request.
        default_value:

    Returns:
        terms if given.
    Raises:
        ValueError: otherwise.
    """
    terms = request.rel_url.query.get("q", default_value)
    return terms
