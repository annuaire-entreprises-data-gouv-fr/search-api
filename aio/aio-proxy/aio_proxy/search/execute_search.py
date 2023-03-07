MAX_TOTAL_RESULTS = 10000


def sort_and_execute_search(
    search,
    offset: int,
    page_size: int,
    is_text_search: bool,
    include_etablissements: bool,
) -> tuple:
    search = search.extra(track_scores=True)
    search = search.extra(explain=True)
    # Collapse is used to aggregate the results by siren. It is the consequence of
    # separating large documents into smaller ones
    search = search.update_from_dict({"collapse": {"field": "siren"}})
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
    search_max_total_results = search
    search = search[offset : (offset + page_size)]
    search_results = search.execute()
    total_results = search_results.hits.total.value
    # Due to performance issues when aggregating on filter queries, we use
    # aggregation on total_results only when total_results is lower than
    # 10 000 results. If total_results is higher than 10 000 results,
    # the aggregation causes timeouts on API. We return by default 10 000 results.
    if total_results < MAX_TOTAL_RESULTS:
        search_max_total_results.aggs.metric("by_cluster", "cardinality", field="siren")
        search_results = search_max_total_results.execute()
        total_results = search_results.aggregations.by_cluster.value

    execution_time = search_results.took
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

    return total_results, response, execution_time, include_etablissements
