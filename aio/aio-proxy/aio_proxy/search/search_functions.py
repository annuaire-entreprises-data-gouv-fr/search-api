from aio_proxy.search.helpers import filter_search, sort_and_execute_search
from elasticsearch_dsl import query


def search_text(index, offset: int, page_size: int, **kwargs):
    query_terms = kwargs["terms"]
    s = index.search()
    # Use filters to reduce search results
    s = filter_search(s, filters_to_ignore=["terms"], **kwargs)
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
                                "siren^3",
                                "siret_siege^3",
                                "identifiantAssociationUniteLegale^3",
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
                                "identifiantAssociationUniteLegale^4",
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
                            fields=["liste_enseigne^7", "liste_adresse^7"],
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
                fields=["nom_complet", "geo_adresse", "liste_dirigeants"],
                fuzziness="AUTO",
            ),
        ],
    )
    return sort_and_execute_search(search=s, offset=offset, page_size=page_size)


def search_geo(index, offset: int, page_size: int, **kwargs):
    s = index.search()
    # Use filters to reduce search results
    s = filter_search(s, filters_to_ignore=["lat", "lon", "radius"], **kwargs)
    s = s.filter(
        "geo_distance",
        distance=f'{kwargs["radius"]}km',
        coordonnees={"lat": kwargs["lat"], "lon": kwargs["lon"]},
    )
    return sort_and_execute_search(search=s, offset=offset, page_size=page_size)
