from datetime import timedelta

from app.elastic.parsers.siren import is_siren
from app.elastic.parsers.siret import is_siret


def extract_ul_and_etab_from_es_response(structure):
    structure_dict = structure.to_dict()
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
    Determines whether to retrieve document by ID based on search parameters.
    """
    page_etablissements = es_search_builder.search_params.page_etablissements
    is_siren_query = is_siren(es_search_builder.search_params.terms)

    if is_siren_query and page_etablissements:
        return True
    return False


def get_doc_id_from_page(es_search_builder):
    """
    Generates a document ID based on search parameters.
    """
    query_terms = es_search_builder.search_params.terms
    page_etablissements = es_search_builder.search_params.page_etablissements
    return f"{query_terms}-{compute_doc_id(page_etablissements)}"


def compute_doc_id(page_etablissements):
    """
    Calculates the page ID based on the number of etablissements.

    Args:
        page_etablissements (int): The page number.

    Returns:
        int: The calculated page ID.
    """
    return page_etablissements * 100


def sort_search_by_company_size(es_search_builder):
    return es_search_builder.search_params.sort_by_size is True


def get_cache_time_to_live(search_params):
    """
    Determine how long to cache search results based on search parameters.

    Args:
        search_params: Search parameters object containing query terms

    Returns:
        timedelta: How long to cache the results
    """
    try:
        query_terms = search_params.terms

        # Cache SIREN/SIRET lookups longer since they're exact matches
        # and this data changes less frequently
        if is_siren(query_terms) or is_siret(query_terms):
            return timedelta(minutes=30)

        # For regular text searches, cache for a shorter period
        return timedelta(hours=24)

    except (AttributeError, KeyError):
        return timedelta(minutes=15)
