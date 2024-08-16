from elasticsearch_dsl import Q


def filter_by_siret(search, siret_string):
    """Filter by 'siret' number"""
    siret_filter = {
        "nested": {
            "path": "unite_legale.etablissements",
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"unite_legale.etablissements.siret": siret_string}}
                    ]
                }
            },
            "inner_hits": {},
        }
    }
    search = search.query(Q(siret_filter))
    return search
