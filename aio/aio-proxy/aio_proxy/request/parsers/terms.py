def check_short_terms_and_no_param(search_params):
    """Prevent performance issues by refusing query terms less than 3 characters.
    Accept less than 3 characters if at least one parameter is filled.
    Except matching size, because this param always has a default value.

    Args:
        search_params: dict of query parameters

    Raises:
        ValueError.
    """
    min_chars_in_terms = 3
    if (
        search_params.get("terms", None) is not None
        and len(search_params.get("terms", None)) < min_chars_in_terms
        and all(
            val is None
            for val in [
                param_value
                for param, param_value in search_params.items()
                if param not in ["terms", "page", "per_page", "matching_size"]
            ]
        )
    ):
        raise ValueError(
            "3 caractères minimum pour les termes de la requête "
            + "(ou utilisez au moins un filtre)"
        )
