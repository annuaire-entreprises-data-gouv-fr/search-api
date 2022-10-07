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


def check_no_param_and_length_terms(params):
    """Prevent performance issues by refusing query terms less than 3 caracters.
    Accept less than 3 caracters if at least one parameter is filled.

    Args:
        params: dict of query parameters

    Raises:
        ValueError.
    """
    if len(params["terms"]) < 3 and all(
        val is None for val in [params[x] for x in params if x != "terms"]
    ):
        raise ValueError(
            "3 caractères minimum pour les termes de la requête "
            + "(ou utilisez au moins un filtre)"
        )
