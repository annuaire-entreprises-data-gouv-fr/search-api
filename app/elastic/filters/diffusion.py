from elasticsearch.dsl import Q

from app.service.siren_protege import siren_protege_list


def build_protege_query():
    """Match documents protected in the index or in the in-memory list."""
    should = [Q("term", **{"unite_legale.est_protege": True})]
    sirens = siren_protege_list.sirens_not_flagged_in_index
    if sirens:
        should.append(Q("terms", **{"unite_legale.siren": list(sirens)}))
    return Q("bool", should=should, minimum_should_match=1)


def build_non_diffusible_query():
    """Match documents to treat as non-diffusible: statut "P" or protected."""
    return Q(
        "bool",
        should=[
            Q("term", **{"unite_legale.statut_diffusion_unite_legale": "P"}),
            build_protege_query(),
        ],
        minimum_should_match=1,
    )
