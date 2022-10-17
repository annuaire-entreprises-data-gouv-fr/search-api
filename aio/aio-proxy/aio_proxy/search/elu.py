from elasticsearch_dsl import query


def search_elus(search, **params):
    elu_filters = []
    boost_queries = []

    # Nom
    nom_elu = params.get("nom_elu", None)
    if nom_elu:
        # match queries returns any document containing the search item,
        # even if it contains another item
        for nom in nom_elu.split(" "):
            elu_filters.append({"match": {"colter_elus.nom": nom}})
        # match_phrase on the name `keyword` makes sure to boost the documents
        # with the exact match
        # Example : search query "jean", the `match` will give "jean pierre" and
        # "jean" the same score. The match_phrase used with a 'should' query will
        # boost "jean" (the exact match) over "jean pierre"
        boost_queries.append(
            {
                "match_phrase": {
                    "colter_elus.nom.keyword": {"query": nom_elu, "boost": 8}
                }
            }
        )

    # Prénoms
    prenoms_elu = params.get("prenoms_elu", None)
    if prenoms_elu:
        # Same logic as "nom" is used for "prenoms"
        for prenom in prenoms_elu.split(" "):
            elu_filters.append({"match": {"colter_elus.prenom": prenom}})
        boost_queries.append(
            {
                "match_phrase": {
                    "colter_elu.prenom.keyword": {
                        "query": prenoms_elu,
                        "boost": 8,
                    }
                }
            }
        )

    # Using a query (must and should) instead of a filter because filters do not give
    # a score which in turn does not boost certain documents over others.
    # The `must` parameter removes documents which do not contain the query terms,
    # whereas the `should` clause gives higher scores to those documents without
    # removing the other documents.
    # Consequently, we use the `must` to find only the documents containing the query
    # terms, and use the `should` clause, with keyword, to give a higher score to exact
    # matches
    if elu_filters or boost_queries:
        search = search.query(
            "nested",
            path="colter_elus",
            query=query.Bool(must=elu_filters, should=boost_queries),
        )
    return search
