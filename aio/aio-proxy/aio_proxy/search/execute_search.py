from typing import Tuple


def sort_and_execute_search(
    search,
    offset: int,
    page_size: int,
    is_search_fields,
) -> Tuple:
    search = search.extra(track_scores=True)
    search = search.extra(explain=True)
    # Sorting is very heavy on performance if there is no
    # search terms (only filters). As there is no search terms, we can
    # exclude this sorting because score is the same for all results
    # documents. Beware, nom and prenoms are search fields.
    if is_search_fields:
        search = search.sort(
            {"_score": {"order": "desc"}},
            {"etat_administratif_unite_legale": {"order": "asc"}},
        )

    search = search[offset : (offset + page_size)]
    results = search.execute()
    total_results = results.hits.total.value
    response = []
    for matched_company in results.hits:
        matched_company_dict = matched_company.to_dict(
            skip_empty=False, include_meta=False
        )
        # Add meta field to response to retrieve score
        matched_company_dict["meta"] = matched_company.meta.to_dict()
        # Add inner hits field (etablissements)
        try:
            matched_etablissements = matched_company.meta.inner_hits.etablissements.hits
            matched_company_dict["inner_hits"] = []
            for matched_etablissement in matched_etablissements:
                matched_company_dict["inner_hits"].append(
                    matched_etablissement.to_dict()
                )
        except Exception:
            matched_company_dict["inner_hits"] = []
        response.append(matched_company_dict)
    return total_results, response
