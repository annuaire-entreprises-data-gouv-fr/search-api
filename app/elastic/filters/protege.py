from elasticsearch.dsl import Q


def exclude_protege_legacy(search):
    """Exclude an unité légale whose address is in the protected legacy list."""
    return search.filter(
        "bool", must_not=[Q("term", **{"unite_legale.est_protege_legacy": True})]
    )
