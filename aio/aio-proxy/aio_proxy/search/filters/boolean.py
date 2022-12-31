from aio_proxy.search.helpers import get_es_field
from elasticsearch_dsl import Q


def filter_search_by_bool_variables_unite_legale(
    search, filters_to_process: list, **params
):
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_process:
            if param_value:
                search = search.filter("exists", field=get_es_field(param_name))
            else:
                search = search.filter(
                    "bool", must_not=[Q("exists", field=get_es_field(param_name))]
                )
    return search


def filter_search_by_bool_variables_etablissements(
    search, filters_to_process: list, **params
):
    """
    The parameters concerned by this function are bool variables that have a
    `TRUE` value when they exist, and are not indexed (in elasticsearch) when the
    value is missing, which is equivalent to having a `FALSE` value.
    e.g "convention_collective_renseignee",
        "est_finess",
        "est_uai",
        "est_entrepreneur_spectacle",
        "est_rge",
    In order to keep the elasticsearch index light, when the value is present for
    these variables, we index `TRUE`, and when the value is missing (meaning it's
    False), we do not index the value `FALSE`, we simply leave it empty.
    Instead, we use this function to filter these values, based on whether a
    value was indexed.
    Having a value equals >> TRUE and not having an indexed value equals >> FALSE.
    We use the "exists" elasticsearch filter to implement it.
    """
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_process:
            field = get_es_field(param_name)
            if param_value:
                exists_query = {
                    "nested": {
                        "path": "etablissements",
                        "query": {
                            "bool": {
                                "must": [
                                    {"exists": {"field": "etablissements." + field}}
                                ]
                            }
                        },
                        "inner_hits": {},
                    }
                }
                search = search.query(Q(exists_query))
            else:
                not_exists_query = {
                    "nested": {
                        "path": "etablissements",
                        "query": {
                            "bool": {
                                "must_not": [
                                    {"exists": {"field": "etablissements." + field}}
                                ]
                            }
                        },
                        "inner_hits": {},
                    }
                }
                search = search.query(Q(not_exists_query))
    return search
