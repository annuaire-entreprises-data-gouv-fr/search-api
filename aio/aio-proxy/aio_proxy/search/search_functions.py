from aio_proxy.search.filters import (
    filter_by_siren,
    filter_by_siret,
    filter_search,
    filter_search_by_bool_variables_etablissements,
    filter_search_by_bool_variables_unite_legale,
    filter_search_by_matching_ids,
)
from aio_proxy.search.helpers import is_siren, is_siret, sort_and_execute_search
from aio_proxy.search.person import search_person
from aio_proxy.search.text import build_text_query
from elasticsearch_dsl import Q


def search_text(index, offset: int, page_size: int, **params):
    query_terms = params["terms"]
    s = index.search()

    # Filter by siren first (if query is a `siren` number), and return search results
    # directly
    if is_siren(query_terms):
        query_terms_clean = query_terms.replace(" ", "")
        s = filter_by_siren(s, query_terms_clean)
        return sort_and_execute_search(
            search=s, offset=offset, page_size=page_size, is_search_fields=False
        )

    # Filter by siret first (if query is a `siret` number), and return search results
    # directly.
    if is_siret(query_terms):
        query_terms_clean = query_terms.replace(" ", "")
        s = filter_by_siret(s, query_terms_clean)
        return sort_and_execute_search(
            search=s, offset=offset, page_size=page_size, is_search_fields=False
        )

    # Use filters to reduce search results
    s = filter_search(
        s,
        filters_to_ignore=[
            "convention_collective_renseignee",
            "est_association",
            "est_finess",
            "est_uai",
            "est_collectivite_territoriale",
            "est_entrepreneur_spectacle",
            "est_rge",
            "id_convention_collective",
            "id_uai",
            "id_finess",
            "id_rge",
            "nom_personne",
            "prenoms_personne",
            "min_date_naiss_personne",
            "max_date_naiss_personne",
            "terms",
            "type_personne",
        ],
        **params,
    )

    # Boolean filters for unité légale
    s = filter_search_by_bool_variables_unite_legale(
        s,
        filters_to_process=[
            "est_association",
            "est_collectivite_territoriale",
        ],
        **params,
    )

    # Boolean filters for établissements
    s = filter_search_by_bool_variables_etablissements(
        s,
        filters_to_process=[
            "convention_collective_renseignee",
            "est_finess",
            "est_uai",
            "est_entrepreneur_spectacle",
            "est_rge",
        ],
        **params,
    )

    # Match ids
    s = filter_search_by_matching_ids(
        s,
        filters_to_process=[
            "id_convention_collective",
            "id_uai",
            "id_finess",
            "id_rge",
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

    # Search text
    if query_terms:
        s = s.query(Q(build_text_query(query_terms)))

    is_search_fields = False
    for item in [
        "terms",
        "nom_personne",
        "prenoms_personne",
    ]:
        if params[item]:
            is_search_fields = True

    return sort_and_execute_search(
        search=s,
        offset=offset,
        page_size=page_size,
        is_search_fields=is_search_fields,
    )


def search_geo(index, offset: int, page_size: int, **params):
    s = index.search()
    # Use filters to reduce search results
    s = filter_search(s, filters_to_ignore=["lat", "lon", "radius"], **params)
    geo_query = {
        "nested": {
            "path": "etablissements",
            "query": {
                "bool": {
                    "filter": {
                        "geo_distance": {
                            "distance": f"{params['radius']}km",
                            "etablissements.coordonnees": {
                                "lat": params["lat"],
                                "lon": params["lon"],
                            },
                        }
                    }
                }
            },
            "inner_hits": {},
        }
    }
    s = s.query(Q(geo_query))
    """
    s = s.filter(
        "geo_distance",
        distance=f'{params["radius"]}km',
        coordonnees={"lat": params["lat"], "lon": params["lon"]},
    )
    """
    return sort_and_execute_search(
        search=s, offset=offset, page_size=page_size, is_search_fields=True
    )
