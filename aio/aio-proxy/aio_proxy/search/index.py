from aio_proxy.search.helpers import CURRENT_COLOR
from elasticsearch_dsl import Document


class ElasticsearchSireneIndex(Document):
    """

    Model-like class for persisting documents in elasticsearch.
    It's a wrapper around document to create specific mappings and to add settings in
    elasticsearch.

    Class used to represent a company headquarters,
    one siren number and the corresponding headquarters siret number

    """

    class Index:
        name = f"siren-{CURRENT_COLOR}"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
