from elasticsearch_dsl import query


def search_dirigeant(search, **params):
    dirigeants_filters = []
    boost_queries = []

    # Nom
    nom_dirigeant = params.get("nom_dirigeant", None)
    if nom_dirigeant:
        # match queries returns any document containing the search item,
        # even if it contains another item
        for nom in nom_dirigeant.split(" "):
            dirigeants_filters.append({"match": {"dirigeants_pp.nom": nom}})
        # match_phrase on the name `keyword` makes sure to boost the documents
        # with the exact match
        # Example : search query "jean", the `match` will give "jean pierre" and
        # "jean" the same score. The match_phrase used with a 'should' query will
        # boost "jean" (the exact match) over "jean pierre"
        boost_queries.append(
            {
                "match_phrase": {
                    "dirigeants_pp.nom.keyword": {"query": nom_dirigeant, "boost": 8}
                }
            }
        )

    # Prénoms
    prenoms_dirigeant = params.get("prenoms_dirigeant", None)
    if prenoms_dirigeant:
        # Same logic as "nom" is used for "prenoms"
        for prenom in prenoms_dirigeant.split(" "):
            dirigeants_filters.append({"match": {"dirigeants_pp.prenoms": prenom}})
        boost_queries.append(
            {
                "match_phrase": {
                    "dirigeants_pp.prenoms.keyword": {"query": prenoms_dirigeant, "boost": 8}
                }
            }
        )

    # Date de naissance
    min_date_naiss_dirigeant = params.get("min_date_naiss_dirigeant", None)
    if min_date_naiss_dirigeant:
        dirigeants_filters.append(
            {
                "range": {
                    **{
                        "dirigeants_pp.date_naissance": {
                            "gte": min_date_naiss_dirigeant
                        }
                    }
                }
            }
        )

    max_date_naiss_dirigeant = params.get("max_date_naiss_dirigeant", None)
    if max_date_naiss_dirigeant:
        dirigeants_filters.append(
            {
                "range": {
                    **{
                        "dirigeants_pp.date_naissance": {
                            "lte": max_date_naiss_dirigeant
                        }
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
    if dirigeants_filters or boost_queries:
        search = search.query(
            "nested",
            path="dirigeants_pp",
            query=query.Bool(must=dirigeants_filters, should=boost_queries),
        )
    return search
