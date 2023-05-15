from aio_proxy.search.execute_search import sort_and_execute_search
from aio_proxy.search.filters.term_filters import filter_term_list_search_unite_legale
from elasticsearch_dsl import Q


def geo_search(index, search_params):
    search_client = index.search()
    geo_search_params = search_params.params

    # Always apply this filter in geo search to prevent displaying non-diffusible
    # data
    search_client = search_client.filter(
        "term", **{"statut_diffusion_unite_legale": "O"}
    )

    # Use filters to reduce search results
    search_client = filter_term_list_search_unite_legale(
        search_client,
        geo_search_params,
        filters_to_include=[
            "activite_principale_unite_legale",
            "section_activite_principale",
        ],
    )
    geo_query = {
        "nested": {
            "path": "etablissements",
            "query": {
                "bool": {
                    "filter": {
                        "geo_distance": {
                            "distance": f"{geo_search_params.radius}km",
                            "etablissements.coordonnees": {
                                "lat": geo_search_params.lat,
                                "lon": geo_search_params.lon,
                            },
                        },
                    }
                }
            },
            "inner_hits": {
                "size": geo_search_params.matching_size,
            },
        }
    }
    search_client = search_client.query(Q(geo_query))

    # By default, exclude etablissements list from response
    include_etablissements = geo_search_params.inclure_etablissements
    if not include_etablissements:
        search_client = search_client.source(excludes=["etablissements"])
    # By default, exclude etablissements list from response
    return sort_and_execute_search(
        search=search_client,
        search_params=geo_search_params,
        is_text_search=True,
    )
