import logging

from aio_proxy.search.parsers.siren import is_siren


def extract_ul_and_etab_from_es_response(structure):
    structure_dict = structure.to_dict(skip_empty=False, include_meta=False)
    # Add meta field to response to retrieve score
    structure_dict["meta"] = structure.meta.to_dict()
    # Add inner hits field (etablissements)
    try:
        matching_etablissements = structure_dict["meta"]["inner_hits"][
            "unite_legale.etablissements"
        ]["hits"]["hits"]
        structure_dict["matching_etablissements"] = []
        for matching_etablissement in matching_etablissements:
            structure_dict["matching_etablissements"].append(
                matching_etablissement["_source"].to_dict()
            )
    except Exception:
        structure_dict["matching_etablissements"] = []
    return structure_dict


def execute_and_agg_total_results_by_identifiant(es_search_builder):
    es_search_client = es_search_builder.es_search_client
    es_search_client.aggs.metric("by_cluster", "cardinality", field="identifiant")
    es_search_client = page_through_results(es_search_builder)
    es_search_client = es_search_client.execute()
    es_search_builder.total_results = es_search_client.aggregations.by_cluster.value
    es_search_builder.execution_time = es_search_client.took


def page_through_results(es_search_builder):
    """

    Args:
        es_search_builder: ElasticSearchBuilder Instance

    Returns:
        ElasticSearchBuilder Instance with pagination

    """
    size = es_search_builder.search_params.per_page
    offset = (es_search_builder.search_params.page - 1) * size
    search_client = es_search_builder.es_search_client
    return search_client[offset : (offset + size)]


def should_get_doc_by_id(es_search_builder):
    """
    Determine whether the search results should be aggregated by `siren`.

    If the `include_admin` option is provided, and it contains "ALL_ETABLISSEMENTS",
    results should not be grouped by `siren` to retrieve all nested `etablissements`.
    Otherwise, results should be aggregated by `siren`.

    Args:
        es_search_builder: An Elasticsearch search builder object.

    Returns:
        bool: True if results should be aggregated by `siren`, False otherwise.
    """
    include_admin = es_search_builder.search_params.include_admin
    should_return_all_etabs = (
        "ALL_ETABLISSEMENTS" not in include_admin if include_admin else True
    )
    page_etablissements = es_search_builder.search_params.page_etablissements
    query_terms = es_search_builder.search_params.terms
    if is_siren(query_terms) and page_etablissements and should_return_all_etabs:
        return True
    return False


def get_doc_id_from_page(es_search_builder):
    query_terms = es_search_builder.search_params.terms
    page_etablissements = es_search_builder.search_params.page_etablissements
    logging.warning(f"%%%%%%%%%%%%%{query_terms}-{page_etablissements*100}")
    return f"{query_terms}-{page_etablissements*100}"
