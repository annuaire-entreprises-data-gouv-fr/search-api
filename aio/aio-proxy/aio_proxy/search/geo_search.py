from aio_proxy.search.execute_search import sort_and_execute_search
from aio_proxy.search.filters.term_filters import filter_term_search_unite_legale
from elasticsearch_dsl import Q


def geo_search(index, offset: int, page_size: int, **params):
    s = index.search()
    # Use filters to reduce search results
    s = filter_term_search_unite_legale(
        s,
        filters_to_include=[
            "activite_principale_unite_legale",
            "section_activite_principale",
        ],
        **params,
    )
    geo_query = {
        "nested": {
            "path": "etablissements",
            "query": {
                "bool": {
                    "filter": {
                        "geo_distance": {
                            "distance": f"{params['radius']}km",
                            "etablissements.coordonnees": {
                                "lat": params["lat"],
                                "lon": params["lon"],
                            },
                        }
                    }
                }
            },
            "inner_hits": {},
        }
    }
    s = s.query(Q(geo_query))
    return sort_and_execute_search(
        search=s, offset=offset, page_size=page_size, is_search_fields=True
    )
