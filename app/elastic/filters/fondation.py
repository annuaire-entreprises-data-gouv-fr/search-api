from app.elastic.queries.fondation import (
    FONDATION_NUMERO_RNF,
    FONDATION_STRUCTURE_TYPE,
)


def filter_fondations(search):
    """Keep the structures that are a fondation."""
    return search.filter("term", type_structure=FONDATION_STRUCTURE_TYPE)


def filter_by_numero_rnf(search, numero_rnf: str):
    """Filter by numéro RNF."""
    return search.filter("term", **{FONDATION_NUMERO_RNF: numero_rnf})
