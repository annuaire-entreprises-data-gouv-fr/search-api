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


def check_short_terms_and_no_param(params):
    """Prevent performance issues by refusing query terms less than 3 characters.
    Accept less than 3 characters if at least one parameter is filled.

    Args:
        params: dict of query parameters

    Raises:
        ValueError.
    """
    if (
        params["terms"] is not None
        and len(params["terms"]) < 3
        and all(
            val is None
            for val in [
                params[x] for x in params if x != "terms" and x != "matching_size"
            ]
        )
    ):
        raise ValueError(
            "3 caractères minimum pour les termes de la requête "
            + "(ou utilisez au moins un filtre)"
        )
