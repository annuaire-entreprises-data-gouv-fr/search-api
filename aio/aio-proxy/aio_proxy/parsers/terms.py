def parse_and_validate_terms(request) -> str:
    """Extract search terms from request.

    Args:
        request: HTTP request.

    Returns:
        terms if given.
    Raises:
        ValueError: otherwise.
    """
    try:
        terms = request.rel_url.query["q"]
        return terms
    except KeyError:
        raise ValueError(
            "Veuillez indiquer la requête avec le paramètre: ?q=ma+recherche."
        )
