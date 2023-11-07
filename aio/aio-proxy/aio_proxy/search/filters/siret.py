from elasticsearch_dsl import Q


def filter_by_siret(search, siret_string):
    """Filter by 'siret' number"""
    siret_filter = {
        "term": {"unite_legale.etablissements.siret": siret_string}
    }
    search = search.query(Q(siret_filter))
    return search
