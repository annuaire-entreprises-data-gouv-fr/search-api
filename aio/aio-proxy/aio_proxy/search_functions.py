from elasticsearch_dsl import Search, query
import json
import requests


def ban_words(terms):
    terms = terms.lower()
    terms = terms.split(' ')
    bans = ['rue', 'avenue', 'de', 'la', 'le', 'du']
    terms = list(set(terms) - set(bans))
    return ' '.join(terms)


def get_result(hit):
    result = {}
    if (hit['_score'] is not None):
        result['_score'] = hit['_score']
    if ('siren' in hit['_source']):
        result['siren'] = hit['_source']['siren']
    if ('nom_complet' in hit['_source']):
        result['nom_complet'] = hit['_source']['nom_complet']
    if ('geo_adresse' in hit['_source']):
        result['geo_adresse'] = hit['_source']['geo_adresse']
    if ('nombre_etablissements' in hit['_source']):
        result['nombre_etablissements'] = str(hit['_source']['nombre_etablissements'])
    if ('identifiantAssociationUniteLegale' in hit['_source']):
        result['identifiantAssociationUniteLegale'] = str(hit['_source']['identifiantAssociationUniteLegale'])
    return result


def is_adress(terms):
    l1 = terms.split(' ')
    l1 = [x.lower() for x in l1]
    l2 = ['rue', 'avenue', 'route', 'boulevard', 'r', 'av', 'bvd', 'bv', 'av', 'voie', 'chemin', 'place', 'pl']
    check = any(item in l2 for item in l1)
    if check:
        headers = {
            "Content-Type": "application/json"
        }
        r = requests.get('https://api-adresse.data.gouv.fr/search/?q=' + terms, headers=headers)

        if (r.status_code == 200):
            if (len(r.json()['features']) > 0):
                if (r.json()['features'][0]['properties']['score'] > 0.8):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

    # add a timeout case 500ms (maybe 200ms)


def search_by_adress(index, query: str, offset: int, page_size: int):
    query = ban_words(query)
    s = index.search()
    s = s.query('match', geo_adresse=query)  # .analyzer(using=annuaire_analyzer)
    s = s.sort({"etat_administratif_etablissement": {'order': "asc"}}, "_score")
    s = s[offset:(offset + page_size)]
    # s = s.highlight('siren', fragment_size=500)
    rs = s.execute()
    total_results = rs.hits.total.value
    res = [hit.to_dict(skip_empty=False) for hit in rs.hits]
    return total_results, res


def search_by_partial_id(index, query: str, field: str, offset: int, page_size: int):
    s = index.search()
    s = s.query({"prefix": {field: {"value": query}}})
    s = s.sort({"etat_administratif_etablissement": {'order': "asc"}}, {"nombre_etablissements": {'order': "desc"}})
    s = s[offset:(offset + page_size)]
    rs = s.execute()
    total_results = rs.hits.total.value
    res = [hit.to_dict(skip_empty=False, include_meta=False) for hit in rs.hits]
    return total_results, res


def search_by_exact_id(index, field: str, query: str, offset: int, page_size: int):  # index: Type[Siren]
    s = index.search()
    s = s.query({"term": {field: {"value": query}}})
    s = s.sort({"etat_administratif_etablissement": {'order': "asc"}}, {"nombre_etablissements": {'order': "desc"}})
    s = s[offset:(offset + page_size)]
    rs = s.execute()
    total_results = rs.hits.total.value
    res = [hit.to_dict(skip_empty=False, include_meta=False) for hit in rs.hits]
    return total_results, res


def is_id(index, query, offset: int, page_size: int):
    for t in query.split(' '):
        try:
            int(t)
            if len(t) >= 9:
                if len(t) == 9:
                    # recherche exact
                    result = search_by_exact_id(index, field='siren', query=query, offset=offset, page_size=page_size)
                    if result:
                        return result
                else:
                    if (len(t) < 14) & (len(t) > 6):
                        # recherche partiel siret
                        result = search_by_partial_id(index, field='siret', query=query, offset=offset, page_size=page_size)
                        if result:
                            return result
                    elif len(t) == 14:
                        # recherche exact siret
                        result = search_by_exact_id(index, field='siret', query=query, offset=offset, page_size=page_size)
                        if result:
                            return result
            else:  # & (len(t) > 6)
                # recherche partielle
                result = search_by_partial_id(index, field='siren', query=query, offset=offset, page_size=page_size)
                if result:
                    return result
        except:
            if len(t) <= 0:
                pass
            else:
                if t[0] == 'W':
                    try:
                        int(t[1:])
                        if len(t) == 10:
                            result = search_by_exact_id(index, field='identifiantAssociationUniteLegale', query=query, offset=offset, page_size=page_size)
                            if not result:
                                pass
                            else:
                                return result
                        elif len(t) < 10:
                            result = search_by_partial_id(index, field='identifiantAssociationUniteLegale', query=query, offset=offset, page_size=page_size)
                            if result:
                                return result
                    except:
                        pass
            pass
    return []


def search_by_name(index, query_terms: str, offset: int, page_size: int):
    s = index.search()
    s = s.query('bool', should=[
        query.Q(
            'function_score',
            query=query.Bool(should=[query.MultiMatch(query=query_terms, type='phrase',
                                                      fields=['nom_complet^15', 'siren^3', 'siret^3',
                                                              'identifiantAssociationUniteLegale^3'])]),
            functions=[
                query.SF("field_value_factor", field="nombre_etablissements", factor=5, modifier='sqrt', missing=1),
            ],
        ),
        query.Match(nom_complet={"query": query_terms})  # , 'fuzziness': 'AUTO'
    ])
    s = s.sort({"etat_administratif_etablissement": {'order': "asc"}}, {"nombre_etablissements": {'order': "desc"}})
    s = s[offset:(offset + page_size)]
    rs = s.execute()
    total_results = rs.hits.total.value
    res = [hit.to_dict(skip_empty=False, include_meta=False) for hit in rs.hits]
    return total_results, res


def search_es(index, query: str, offset: int, page_size: int):
    isid = is_id(index, query, offset, page_size)
    if len(isid) == 0:
        isadress = is_adress(query)
        if isadress:
            result = search_by_adress(index, query=query, offset=offset, page_size=page_size)
        else:
            result = search_by_name(index, query_terms=query, offset=offset, page_size=page_size)
        return result
    else:
        return isid
