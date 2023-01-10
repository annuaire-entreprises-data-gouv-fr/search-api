from aio_proxy.search.helpers.elastic_fields import get_elasticsearch_field_name


def filter_term_search_unite_legale(search, filters_to_include: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_include:
            search = search.filter(
                "term", **{get_elasticsearch_field_name(param_name): param_value}
            )
    return search


def filter_term_list_search_unite_legale(search, filters_to_include: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_include:
            search = search.filter(
                "terms", **{get_elasticsearch_field_name(param_name): param_value}
            )
    return search
