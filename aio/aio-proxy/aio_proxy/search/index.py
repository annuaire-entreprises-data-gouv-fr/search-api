from aio_proxy.search.helpers import CURRENT_COLOR
from elasticsearch_dsl import Document


class ElasticsearchSireneIndex(Document):
    """
    Class used to represent a company headquarters,
    one siren number and the corresponding sheadquarters siret number
    """

    class Index:
        name = f"siren-{CURRENT_COLOR}"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
