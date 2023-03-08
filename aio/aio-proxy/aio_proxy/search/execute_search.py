import logging
from datetime import timedelta

from aio_proxy.response.cache.cache import cache_strategy

TIME_TO_LIVE = timedelta(days=31)
MIN_EXECUTION_TIME = 400
MAX_TOTAL_RESULTS = 10000


def execute_and_format_search_response(
    search, offset, page_size, include_etablissements
):
    search_max_total_results = search
    search = search[offset : (offset + page_size)]
    search_results = search.execute()
    total_results = search_results.hits.total.value
    execution_time = search_results.took
    # Due to performance issues when aggregating on filter queries, we use
    # aggregation on total_results only when total_results is lower than
    # 10 000 results. If total_results is higher than 10 000 results,
    # the aggregation causes timeouts on API. We return by default 10 000 results.
    if total_results < MAX_TOTAL_RESULTS:
        search_max_total_results.aggs.metric("by_cluster", "cardinality", field="siren")
        search_max_total_results = search_max_total_results[
            offset : (offset + page_size)
        ]
        search_max_total_results = search_max_total_results.execute()
        total_results = search_max_total_results.aggregations.by_cluster.value
        execution_time = search_max_total_results.took
    response = []
    for matching_unite_legale in search_results.hits:
        matching_unite_legale_dict = matching_unite_legale.to_dict(
            skip_empty=False, include_meta=False
        )
        # Add meta field to response to retrieve score
        matching_unite_legale_dict["meta"] = matching_unite_legale.meta.to_dict()
        # Add inner hits field (etablissements)
        try:
            matching_etablissements = (
                matching_unite_legale.meta.inner_hits.etablissements.hits
            )
            matching_unite_legale_dict["matching_etablissements"] = []
            for matching_etablissement in matching_etablissements:
                matching_unite_legale_dict["matching_etablissements"].append(
                    matching_etablissement.to_dict()
                )
        except Exception:
            matching_unite_legale_dict["matching_etablissements"] = []

        response.append(matching_unite_legale_dict)
    search_response = {
        "total_results": total_results,
        "response": response,
        "execution_time": execution_time,
        "include_etablissements": include_etablissements,
    }
    return search_response


def sort_search(search, is_text_search: bool):
    # Sorting is very heavy on performance if there is no
    # search terms (only filters). As there is no search terms, we can
    # exclude this sorting because score is the same for all results
    # documents. Beware, nom and prenoms are search fields.
    if is_text_search:
        search = search.sort(
            {"_score": {"order": "desc"}},
            {"etat_administratif_unite_legale": {"order": "asc"}},
        )
    # If only filters are used, use nombre établissements ouverts to sort the results
    else:
        search = search.sort(
            {"nombre_etablissements_ouverts": {"order": "desc"}},
        )
    return search


def sort_and_execute_search(
    search,
    offset: int,
    page_size: int,
    is_text_search: bool,
    include_etablissements: bool,
) -> dict:
    search = search.extra(track_scores=True)
    search = search.extra(explain=True)
    # Collapse is used to aggregate the results by siren. It is the consequence of
    # separating large documents into smaller ones
    search = search.update_from_dict({"collapse": {"field": "siren"}})
    search = sort_search(search, is_text_search)

    # Execute search
    def get_search_response():
        return execute_and_format_search_response(
            search,
            offset,
            page_size,
            include_etablissements,
        )

    search_response = cache_strategy(
        search,
        get_search_response,
        should_cache_search_response,
        TIME_TO_LIVE,
    )
    return search_response


def should_cache_search_response(search_response):
    """Cache search response if execution time is higher than 400 ms"""
    try:
        if search_response["execution_time"] > MIN_EXECUTION_TIME:
            return True
        return False
    except KeyError as error:
        logging.info(f"Error getting search execution time: {error}")
        return False
