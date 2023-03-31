from aio_proxy.search.execute_search import sort_and_execute_search
from aio_proxy.search.filters.term_filters import filter_term_list_search_unite_legale
from elasticsearch_dsl import Q


def geo_search(index, offset: int, page_size: int, **params):
    search_client = index.search()

    # always apply this filter to prevent displaying non allowed information
    search_client = search_client.filter(
        "term", **{"statut_diffusion_unite_legale": "O"}
    )

    # Use filters to reduce search results
    search_client = filter_term_list_search_unite_legale(
        search_client,
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
                        },
                    }
                }
            },
            "inner_hits": {
                "size": params["matching_size"],
            },
        }
    }
    search_client = search_client.query(Q(geo_query))

    # By default, exclude etablissements list from response
    include_etablissements = params["inclure_etablissements"]
    if not include_etablissements:
        search_client = search_client.source(exclude=["etablissements"])
    # By default, exclude etablissements list from response
    include_slug = params["inclure_slug"]
    return sort_and_execute_search(
        search=search_client,
        offset=offset,
        page_size=page_size,
        is_text_search=True,
        include_etablissements=include_etablissements,
        include_slug=include_slug,
    )
