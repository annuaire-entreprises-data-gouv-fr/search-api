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
        {"etat_administratif_etablissement": {"order": "asc"}},
    )
    search = search[offset : (offset + page_size)]
    results = search.execute()
    total_results = results.hits.total.value
    response = [
        hit.to_dict(skip_empty=False, include_meta=False) for hit in results.hits
    ]
    return total_results, response
