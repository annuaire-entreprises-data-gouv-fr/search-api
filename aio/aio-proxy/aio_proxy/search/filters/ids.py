from aio_proxy.search.helpers import get_es_field
from elasticsearch_dsl import Q


def filter_search_by_matching_ids(search, filters_to_process: list, **params):
    """Filter search by matching an id in an array of ids.
    e.g ids : "id_convention_collective",
              "id_uai",
              "id_finess",
              "id_rge","""
    for param_name, param_value in params.items():
        if param_value is not None and param_name in filters_to_process:
            field = get_es_field(param_name)
            id_filter = {
                "nested": {
                    "path": "etablissements",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match": {
                                        "etablissements."
                                        + field: {
                                            "query": param_value,
                                            "boost": 10,
                                            "_name": "Filter id:" + field,
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "inner_hits": {},
                }
            }
            search = search.query(Q(id_filter))
    return search
