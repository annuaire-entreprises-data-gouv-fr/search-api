def filter_search(search, filters_to_ignore: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name not in filters_to_ignore:
            search = search.filter("term", **{get_es_field(param_name): param_value})
    return search
