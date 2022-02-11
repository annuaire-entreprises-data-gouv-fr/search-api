from elasticsearch_dsl import Search, query
import json
import requests


def search_by_name(index, query_terms: str, offset: int, page_size: int):
    s = index.search()
    s = s.query('bool', should=[
        query.Q(
            'function_score',
            query=query.Bool(should=[query.MultiMatch(query=query_terms, type='phrase',
                                                      fields=['nom_complet^15', 'siren^3', 'siret^3',
                                                              'identifiantAssociationUniteLegale^3'])]),
            functions=[
                query.SF("field_value_factor", field="nombre_etablissements_ouvert", factor=10, modifier='sqrt',
                         missing=1),
            ],
        ),
        query.Q(
            'function_score',
            query=query.Bool(
                must=[query.Match(concat_nom_adr_siren={"query": query_terms, "operator": "and", "boost": 8})]),
            functions=[
                query.SF("field_value_factor", field="nombre_etablissements_ouvert", factor=10, modifier='sqrt',
                         missing=1),
            ],
        ),
        query.Q(
            'function_score',
            query=query.Bool(should=[query.MultiMatch(
                query=query_terms,
                type='most_fields',
                fields=['nom_complet^7', 'siren^7', 'siret^4', 'identifiantAssociationUniteLegale^4'],
                operator="and")]),
            functions=[
                query.SF("field_value_factor", field="nombre_etablissements_ouvert", factor=10, modifier='sqrt',
                         missing=1),
            ],
        ),

        query.MultiMatch(query=query_terms, type='most_fields', operator="and", fields=['nom_complet', 'geo_adresse'], fuzziness='AUTO')
    ])
    s = s.extra(track_scores=True)
    s = s.sort({"etat_administratif_etablissement": {'order': "asc"}}, {"_score": {'order': "desc"}})
    s = s[offset:(offset + page_size)]
    rs = s.execute()
    total_results = rs.hits.total.value
    res = [hit.to_dict(skip_empty=False, include_meta=False) for hit in rs.hits]
    return total_results, res


def search_es(index, query: str, offset: int, page_size: int):
    result = search_by_name(index, query_terms=query, offset=offset, page_size=page_size)
    return result
