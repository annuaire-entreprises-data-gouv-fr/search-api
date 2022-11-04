from aio_proxy.search.helpers import get_es_field
from elasticsearch_dsl import Q


def filter_by_siren(search, siren_string):
    """Filter by `siren` number"""
    search = search.filter("term", **{"siren": siren_string})
    return search


def filter_search(search, filters_to_ignore: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name not in filters_to_ignore:
            search = search.filter("term", **{get_es_field(param_name): param_value})
    return search


def filter_search_is_exist(search, filters_to_process: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_process:
            if param_value:
                search = search.filter("exists", field=get_es_field(param_name))
            else:
                search = search.filter(
                    "bool", must_not=[Q("exists", field=get_es_field(param_name))]
                )
    return search


def filter_search_match_array(search, filters_to_process: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_process:
            search = search.filter("match", **{get_es_field(param_name): param_value})
    return search
