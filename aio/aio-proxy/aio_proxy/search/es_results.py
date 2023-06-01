def extract_ul_and_etab_from_es_response(unite_legale):
    unite_legale_dict = unite_legale.to_dict(skip_empty=False, include_meta=False)
    # Add meta field to response to retrieve score
    unite_legale_dict["meta"] = unite_legale.meta.to_dict()
    # Add inner hits field (etablissements)
    try:
        matching_etablissements = unite_legale.meta.inner_hits.etablissements.hits
        unite_legale_dict["matching_etablissements"] = []
        for matching_etablissement in matching_etablissements:
            unite_legale_dict["matching_etablissements"].append(
                matching_etablissement.to_dict()
            )
    except Exception:
        unite_legale_dict["matching_etablissements"] = []
    return unite_legale_dict


def execute_and_agg_total_results_by_siren(es_builder, es_search_client):
    es_search_client.aggs.metric("by_cluster", "cardinality", field="siren")
    es_search_client = page_through_results(es_builder, es_search_client)
    es_search_client = es_search_client.execute()
    es_builder.total_results = es_search_client.aggregations.by_cluster.value
    es_builder.execution_time = es_search_client.took


def page_through_results(es_search_builder, es_search_client):
    """

    Args:
        es_search_builder: ElasticSearchBuilder Instance
        es_search_client: Elasticsearch Client

    Returns:
        Elasticsearch client with pagination

    """
    offset = es_search_builder.search_params.page
    size = es_search_builder.search_params.per_page
    return es_search_client[offset : (offset + size)]
