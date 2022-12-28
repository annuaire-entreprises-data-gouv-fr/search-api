from aio_proxy.search.helpers import get_es_field
from elasticsearch_dsl import Q, Nested


def filter_by_siren(search, siren_string):
    """Filter by `siren` number"""
    search = search.filter("term", **{"siren": siren_string})
    return search


def filter_by_siret(search, siret_string):
    """Filter by 'siret' number"""
    siret_filter = {
        "nested": {
            "path": "etablissements",
            "query": {
                "bool": {
                    "filter": [
                  {
                    "term": {
                      "etablissements.siret": siret_string
                    }
                  }
                ]
              }
            },
            "inner_hits": {}
          }
    }
    search = search.query(Q(siret_filter))
    return search


def filter_search(search, filters_to_ignore: list, **params):
    """Use filters to reduce search results."""
    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():
        if param_value is not None and param_name not in filters_to_ignore:
            search = search.filter("term", **{get_es_field(param_name): param_value})
    return search


def filter_search_by_bool_variables(search, filters_to_process: list, **params):
    """
    The parameters concerned by this function are bool variables that have a
    `TRUE` value when they exist, and are not indexed (in elasticsearch) when the
    value is missing, which is equivalent to having a `FALSE` value.
    e.g "convention_collective_renseignee",
        "est_finess",
        "est_uai",
        "est_collectivite_territoriale",
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
            if param_value:
                search = search.filter("exists", field=get_es_field(param_name))
            else:
                search = search.filter(
                    "bool", must_not=[Q("exists", field=get_es_field(param_name))]
                )
    return search


def filter_search_by_matching_ids(search, filters_to_process: list, **params):
    """Filter search by matching an id in an array of ids.
    e.g ids : "id_convention_collective",
              "id_uai",
              "id_finess",
              "id_rge","""
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_process:
            search = search.filter("match", **{get_es_field(param_name): param_value})
    return search
