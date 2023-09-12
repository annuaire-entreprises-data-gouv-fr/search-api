from aio_proxy.search.filters.term_filters import filter_term_list_search_unite_legale
from elasticsearch_dsl import Q


def build_es_search_geo_query(es_search_builder):
    # Always apply this filter in geo search to prevent displaying non-diffusible
    # data
    es_search_builder.es_search_client = es_search_builder.es_search_client.filter(
        "term", **{"unite_legale.statut_diffusion_unite_legale": "O"}
    )

    # Use filters to reduce search results
    es_search_builder.es_search_client = filter_term_list_search_unite_legale(
        es_search_builder.es_search_client,
        es_search_builder.search_params,
        filters_to_include=[
            "activite_principale_unite_legale",
            "section_activite_principale",
        ],
    )
    geo_query = {
        "nested": {
            "path": "unite_legale.etablissements",
            "query": {
                "bool": {
                    "filter": {
                        "geo_distance": {
                            "distance": f"{es_search_builder.search_params.radius}km",
                            "unite_legale.etablissements.coordonnees": {
                                "lat": es_search_builder.search_params.lat,
                                "lon": es_search_builder.search_params.lon,
                            },
                        },
                    }
                }
            },
            "inner_hits": {
                "size": es_search_builder.search_params.matching_size,
            },
        }
    }
    es_search_builder.es_search_client = es_search_builder.es_search_client.query(
        Q(geo_query)
    )

    # By default, exclude etablissements list from response
    include_atablissements = (
        es_search_builder.search_params.include_admin
        and "ETABLISSEMENTS" in es_search_builder.search_params.include_admin
    )

    if not include_atablissements:
        es_search_builder.es_search_client = es_search_builder.es_search_client.source(
            excludes=["unite_legale.etablissements"]
        )
    es_search_builder.has_full_text_query = True
