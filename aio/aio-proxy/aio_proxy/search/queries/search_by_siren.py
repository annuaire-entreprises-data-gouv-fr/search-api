from aio_proxy.search.es_index import StructureMapping
from aio_proxy.search.filters.siren import filter_by_siren


def search_by_siren(siren):
    es_client = StructureMapping.search()
    es_client = filter_by_siren(es_client, siren)
    response = es_client.execute()
    if response.hits.total.value > 0:
        return response.hits[0]

    return None
