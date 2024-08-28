from app.elastic.es_search_runner import ElasticSearchRunner
from app.elastic.filters.siren import filter_by_siren


def search_index_by_siren(siren: str):
    es_runner = ElasticSearchRunner()
    # Apply a filter to the search query using the provided SIREN number
    search_query = filter_by_siren(es_runner.es_search_client, siren)
    search_response = search_query.execute()

    # Check if there are any results from the search
    if search_response.hits.total.value > 0:
        return search_response.hits[0]
    return None
