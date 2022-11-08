from aio_proxy.search.filters import (
    filter_by_siren,
    filter_search,
    filter_search_is_exist,
    filter_search_match_array,
)
from aio_proxy.search.helpers import is_siren, sort_and_execute_search
from aio_proxy.search.person import search_person
from elasticsearch_dsl import query


def search_text(index, offset: int, page_size: int, **params):
    query_terms = params["terms"]
    s = index.search()

    # Filter by siren first (if query is a `siren` number), and return search results
    # directly.
    if is_siren(query_terms):
        query_terms_clean = query_terms.replace(" ", "")
        s = filter_by_siren(s, query_terms_clean)
        return sort_and_execute_search(
            search=s, offset=offset, page_size=page_size, is_search_fields=False
        )

    # Use filters to reduce search results
    s = filter_search(
        s,
        filters_to_ignore=[
            "terms",
            "convention_collective_renseignee",
            "est_finess",
            "est_uai",
            "est_collectivite_territoriale",
            "est_entrepreneur_spectacle",
            "est_rge",
            "id_convention_collective",
            "id_uai",
            "id_finess",
            "id_rge",
            "nom_dirigeant",
            "prenoms_dirigeant",
            "min_date_naiss_dirigeant",
            "max_date_naiss_dirigeant",
            "nom_elu",
            "prenoms_elu",
            "min_date_naiss_elu",
            "max_date_naiss_elu",
            "nom_personne",
            "prenoms_personne",
            "min_date_naiss_personne",
            "max_date_naiss_personne",
        ],
        **params,
    )
    s = filter_search_is_exist(
        s,
        filters_to_process=[
            "convention_collective_renseignee",
            "est_finess",
            "est_uai",
            "est_collectivite_territoriale",
            "est_entrepreneur_spectacle",
            "est_rge",
        ],
        **params,
    )
    s = filter_search_match_array(
        s,
        filters_to_process=[
            "id_convention_collective",
            "id_uai",
            "id_finess",
            "id_rge",
        ],
        **params,
    )

    # Search both élus and dirigeants
    s = search_person(
        s,
        "nom_personne",
        "prenoms_personne",
        "min_date_naiss_personne",
        "max_date_naiss_personne",
        [
            {
                "nested_object": "dirigeants_pp",
                "match_nom": "nom",
                "match_prenom": "prenoms",
                "match_date": "date_naissance",
            },
            {
                "nested_object": "colter_elus",
                "match_nom": "nom",
                "match_prenom": "prenom",
                "match_date": "date_naissance",
            },
        ],
        **params,
    )

    # Search text
    if query_terms:
        s = s.query(
            "bool",
            should=[
                query.Q(
                    "function_score",
                    query=query.Bool(
                        should=[
                            query.MultiMatch(
                                query=query_terms,
                                type="phrase",
                                fields=[
                                    "nom_complet^15",
                                    "liste_dirigeants^5",
                                    "siren^3",
                                    "siret_siege^3",
                                    "identifiant_association_unite_legale^3",
                                ],
                            )
                        ]
                    ),
                    functions=[
                        query.SF(
                            "field_value_factor",
                            field="nombre_etablissements_ouverts",
                            factor=10,
                            modifier="sqrt",
                            missing=1,
                        ),
                    ],
                ),
                query.Q(
                    "function_score",
                    query=query.Bool(
                        must=[
                            query.Match(
                                concat_nom_adr_siren={
                                    "query": query_terms,
                                    "operator": "and",
                                    "boost": 8,
                                }
                            )
                        ]
                    ),
                    functions=[
                        query.SF(
                            "field_value_factor",
                            field="nombre_etablissements_ouverts",
                            factor=10,
                            modifier="sqrt",
                            missing=1,
                        ),
                    ],
                ),
                query.Q(
                    "function_score",
                    query=query.Bool(
                        should=[
                            query.MultiMatch(
                                query=query_terms,
                                type="most_fields",
                                fields=[
                                    "nom_complet^7",
                                    "siren^7",
                                    "siret_siege^4",
                                    "identifiant_association_unite_legale^4",
                                ],
                                operator="and",
                            )
                        ]
                    ),
                    functions=[
                        query.SF(
                            "field_value_factor",
                            field="nombre_etablissements_ouverts",
                            factor=10,
                            modifier="sqrt",
                            missing=1,
                        ),
                    ],
                ),
                query.Q(
                    "function_score",
                    query=query.Bool(
                        should=[
                            query.MultiMatch(
                                query=query_terms,
                                type="most_fields",
                                fields=["liste_enseignes^7", "liste_adresses^7"],
                                operator="and",
                            )
                        ]
                    ),
                    functions=[
                        query.SF(
                            "field_value_factor",
                            field="nombre_etablissements_ouverts",
                            factor=10,
                            modifier="sqrt",
                            missing=1,
                        ),
                    ],
                ),
                query.Q(
                    "function_score",
                    query=query.Bool(
                        must=[
                            query.Match(
                                concat_enseigne_adresse={
                                    "query": query_terms,
                                    "operator": "and",
                                    "boost": 8,
                                }
                            )
                        ]
                    ),
                    functions=[
                        query.SF(
                            "field_value_factor",
                            field="nombre_etablissements_ouverts",
                            factor=10,
                            modifier="sqrt",
                            missing=1,
                        ),
                    ],
                ),
                query.MultiMatch(
                    query=query_terms,
                    type="most_fields",
                    operator="and",
                    fields=["nom_complet", "adresse_etablissement", "liste_dirigeants"],
                    fuzziness="AUTO",
                ),
            ],
        )
    is_search_fields = False
    for item in [
        "terms",
        "nom_personne",
        "nom_dirigeant",
        "nom_elu",
        "prenoms_personne",
        "prenoms_dirigeant",
        "prenoms_elu",
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
    s = s.filter(
        "geo_distance",
        distance=f'{params["radius"]}km',
        coordonnees={"lat": params["lat"], "lon": params["lon"]},
    )
    return sort_and_execute_search(
        search=s, offset=offset, page_size=page_size, is_search_fields=True
    )
