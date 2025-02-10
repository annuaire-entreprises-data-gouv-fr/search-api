from app.elastic.parsers.siren import is_siren
from elasticsearch_dsl import A


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
    agg_identifiant_cardinality(es_search_client)
    es_search_client = es_search_client.extra(
        size=0, track_scores=False, track_total_hits=False
    )
    es_search_client = es_search_client.execute()
    es_search_builder.total_results = es_search_client.aggregations.by_cluster.value
    es_search_builder.execution_time += es_search_client.took


def agg_identifiant_cardinality(es_search_builder, sample=False, size=100):
    agg = A("cardinality", field="identifiant")

    if sample:
        sampler = A("sampler", shard_size=size, aggs={"by_cluster": agg})
        es_search_builder.aggs.bucket("sample", sampler)
    else:
        es_search_builder.aggs.metric("by_cluster", agg)


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
