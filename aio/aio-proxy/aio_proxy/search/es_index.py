from elasticsearch_dsl import Document


class StructureMapping(Document):
    """

    Model-like class for persisting documents in elasticsearch.
    It's a wrapper around Document to create specific mappings and to add settings in
    elasticsearch.

    Class used to represent a company headquarters,
    one Siren number and the corresponding Siret numbers.

    """

    class Index:
        name = "siren-reader"
