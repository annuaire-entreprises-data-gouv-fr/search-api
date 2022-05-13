from typing import Tuple


def filter_search(search, filters_to_ignore: list, **kwargs):
    """Use filters to reduce search results."""
    for key, value in kwargs.items():
        if value is not None and key not in filters_to_ignore:
            search = search.filter("term", **{key: value})
    return search


def sort_and_execute_search(search, offset: int, page_size: int) -> Tuple:
    search = search.extra(track_scores=True)
    search = search.sort(
        {"_score": {"order": "desc"}},
        {"etat_administratif_siege": {"order": "asc"}},
    )
    search = search[offset : (offset + page_size)]
    results = search.execute()
    total_results = results.hits.total.value
    response = [
        hit.to_dict(skip_empty=False, include_meta=False) for hit in results.hits
    ]
    return total_results, response


def hide_fields(search_result: list) -> list:
    """Hide concatenation fields in search results."""
    hidden_fields = {
        "coordonnees",
        "concat_nom_adr_siren",
        "concat_enseigne_adresse",
        "geo_adresse",
        "is_siege",
        "liste_adresse",
        "liste_enseigne",
    }
    results = [
        {field: value for field, value in unite.items() if field not in hidden_fields}
        for unite in search_result
    ]
    return results
