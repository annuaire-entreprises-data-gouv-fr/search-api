def filter_by_siren(search, siren_string):
    """Filter by `siren` number"""
    search = search.filter("term", **{"siren": siren_string})
    return search


def filter_search(search, filters_to_ignore: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name not in filters_to_ignore:
            search = search.filter("term", **{param_name: param_value})
    return search


def get_es_field(param_name):
    if param_name == "is_finess":
        return "liste_finess"
    if param_name == "is_uai":
        return "liste_uai"
    if param_name == "is_colter":
        return "colter_code"
    if param_name == "is_entrepreneur_spectacle":
        return "is_entrepreneur_spectacle"
    if param_name == "is_rge":
        return "is_rge"
    if param_name == "idcc":
        return "liste_idcc"
    if param_name == "uai":
        return "liste_uai"
    if param_name == "finess":
        return "liste_finess"
    if param_name == "colter_code_insee":
        return "colter_code_insee"


def filter_search_is_exist(search, filters_to_process: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_process:
            search = search.filter("exists", field=get_es_field(param_name))
    return search


def filter_search_match_array(search, filters_to_process: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_process:
            search = search.filter("match", **{get_es_field(param_name): param_value})
    return search
