import os

from elasticsearch_dsl import Document


class Siren(Document):
    """
    Class used to represent a company headquarters,
    one siren number and the corresponding sheadquarters siret number
    """

    class Index:
        name = f'siren-{os.getenv("CURRENT_COLOR")}'
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
