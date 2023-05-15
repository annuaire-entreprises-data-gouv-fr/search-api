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
    if terms:
        return terms.upper()
    return terms


def check_short_terms_and_no_param(search_params):
    """Prevent performance issues by refusing query terms less than 3 characters.
    Accept less than 3 characters if at least one parameter is filled.
    Except matching size, because this param always has a default value.

    Args:
        params: dict of query parameters

    Raises:
        ValueError.
    """
    min_chars_in_terms = 3
    if (
        search_params.terms is not None
        and len(search_params.terms) < min_chars_in_terms
        and all(
            val is None
            for val in [
                y
                for x, y in vars(search_params).items()
                if x != "terms" and x != "matching_size"
            ]
        )
    ):
        raise ValueError(
            "3 caractères minimum pour les termes de la requête "
            + "(ou utilisez au moins un filtre)"
        )
