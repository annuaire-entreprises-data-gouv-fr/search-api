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
