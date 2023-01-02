from aio_proxy.search.execute_search import sort_and_execute_search
from aio_proxy.search.filters.boolean import filter_search_by_bool_fields_unite_legale
from aio_proxy.search.filters.nested_etablissements_filters import (
    add_nested_etablissements_filters_to_text_query,
    build_nested_etablissements_filters_query_with_inner_hits,
    build_nested_etablissements_filters_query_without_inner_hits,
)
from aio_proxy.search.filters.siren import filter_by_siren
from aio_proxy.search.filters.siret import filter_by_siret
from aio_proxy.search.filters.term_filters import filter_term_search_unite_legale
from aio_proxy.search.helpers.etablissements_filters_used import (
    is_any_etablissement_filter_used,
)
from aio_proxy.search.parsers.siren import is_siren
from aio_proxy.search.parsers.siret import is_siret
from aio_proxy.search.queries.person import search_person
from aio_proxy.search.queries.text import build_text_query
from elasticsearch_dsl import Q


def text_search(index, offset: int, page_size: int, **params):
    query_terms = params["terms"]
    s = index.search()

    # Check if any etablissements filters are used
    etablissement_filter_used = is_any_etablissement_filter_used(**params)

    # Filter by siren first (if query is a `siren` number), and return search results
    # directly without text search.
    if is_siren(query_terms):
        query_terms_clean = query_terms.replace(" ", "")
        s = filter_by_siren(s, query_terms_clean)
        return sort_and_execute_search(
            search=s,
            offset=offset,
            page_size=page_size,
            is_search_fields=False,
        )

    # Filter by siret first (if query is a `siret` number), and return search results
    # directly without text search.
    if is_siret(query_terms):
        query_terms_clean = query_terms.replace(" ", "")
        s = filter_by_siret(s, query_terms_clean)
        return sort_and_execute_search(
            search=s,
            offset=offset,
            page_size=page_size,
            is_search_fields=False,
        )

    # Filter results by term using 'unité légale' related filters in the request
    s = filter_term_search_unite_legale(
        s,
        filters_to_include=[
            "est_entrepreneur_individuel",
            "est_entrepreneur_spectacle",
            "economie_sociale_solidaire_unite_legale",
            "etat_administratif_unite_legale",
            "activite_principale_unite_legale",
            "code_collectivite_territoriale",
            "section_activite_principale",
            "tranche_effectif_salarie_unite_legale",
        ],
        **params,
    )

    # Filters applied on établissements, 1st application of filters before text search
    # to make sure the text_query (on unite légale) is applied only to filtered
    # results.
    # Otherwise, the text_query (with filters injected) will return all unite_legale
    # that match the filter without any regarde to the text_query on unite_legale
    # These filters are applied always, even with a query search, since we do not
    # include inner hits in this particular search query
    if etablissement_filter_used:
        filters_etablissements_query_without_inner_hits = (
            build_nested_etablissements_filters_query_without_inner_hits(**params)
        )
        if filters_etablissements_query_without_inner_hits:
            s = s.query(Q(filters_etablissements_query_without_inner_hits))

    # Filters applied on établissements without text search
    if not query_terms and etablissement_filter_used:
        filters_etablissements_query_with_inner_hits = (
            build_nested_etablissements_filters_query_with_inner_hits(**params)
        )
        if filters_etablissements_query_with_inner_hits:
            s = s.query(Q(filters_etablissements_query_with_inner_hits))

    # Boolean filters for unité légale
    s = filter_search_by_bool_fields_unite_legale(
        s,
        filters_to_include=[
            "est_association",
            "est_collectivite_territoriale",
        ],
        **params,
    )

    # Search 'élus' only
    if params["type_personne"] == "ELU":
        s = search_person(
            s,
            "nom_personne",
            "prenoms_personne",
            "min_date_naiss_personne",
            "max_date_naiss_personne",
            [
                {
                    "type_person": "colter_elus",
                    "match_nom": "nom",
                    "match_prenom": "prenom",
                    "match_date": "date_naissance",
                },
            ],
            **params,
        )

    # Search 'dirigeants' only
    elif params["type_personne"] == "DIRIGEANT":
        s = search_person(
            s,
            "nom_personne",
            "prenoms_personne",
            "min_date_naiss_personne",
            "max_date_naiss_personne",
            [
                {
                    "type_person": "dirigeants_pp",
                    "match_nom": "nom",
                    "match_prenom": "prenoms",
                    "match_date": "date_naissance",
                },
            ],
            **params,
        )
    else:
        # Search both 'élus' and 'dirigeants'
        s = search_person(
            s,
            "nom_personne",
            "prenoms_personne",
            "min_date_naiss_personne",
            "max_date_naiss_personne",
            [
                {
                    "type_person": "dirigeants_pp",
                    "match_nom": "nom",
                    "match_prenom": "prenoms",
                    "match_date": "date_naissance",
                },
                {
                    "type_person": "colter_elus",
                    "match_nom": "nom",
                    "match_prenom": "prenom",
                    "match_date": "date_naissance",
                },
            ],
            **params,
        )

    # Filters applied on établissement with text search
    if query_terms and etablissement_filter_used:
        text_query = build_text_query(query_terms)
        text_query_with_filters = add_nested_etablissements_filters_to_text_query(
            text_query, **params
        )
        s = s.query(Q(text_query_with_filters))

    # Text search only without etablissements filters
    if query_terms and not etablissement_filter_used:
        text_query = build_text_query(query_terms)
        s = s.query(Q(text_query))

    is_search_fields = False
    for item in [
        "terms",
        "nom_personne",
        "prenoms_personne",
    ]:
        if params[item]:
            is_search_fields = True

    # By default, exclude etablissements list from response
    if not params["inclure_etablissements"]:
        s = s.source(exclude=["etablissements"])

    return sort_and_execute_search(
        search=s,
        offset=offset,
        page_size=page_size,
        is_search_fields=is_search_fields,
    )
