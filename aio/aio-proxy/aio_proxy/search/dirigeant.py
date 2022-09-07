from elasticsearch_dsl import query


def search_dirigeant(search, **kwargs):
    dirigeants_filters = []
    boost_queries = []

    for key, value in kwargs.items():
        if key == "nom_dirigeant" and value is not None:
            # match queries returns any document containing the search item,
            # even if it contains another item
            for nom in value.split(" "):
                dirigeants_filters.append({"match": {"dirigeants_pp.nom": nom}})
            # match_phrase on the name `keyword` makes sure to boost the documents
            # with the exact match
            # Example : search query "jean", the `match` will give "jean pierre" and
            # "jean" the same score. The match_phrase used with a 'should' query will
            # boost "jean" (the exact match) over "jean pierre"
            boost_queries.append(
                {
                    "match_phrase": {
                        "dirigeants_pp.nom.keyword": {"query": value, "boost": 8}
                    }
                }
            )

        if key == "prenoms_dirigeant" and value is not None:
            # Same logic as "nom" is used for "prenoms"
            for prenom in value.split(" "):
                dirigeants_filters.append({"match": {"dirigeants_pp.prenoms": prenom}})
            boost_queries.append(
                {
                    "match_phrase": {
                        "dirigeants_pp.prenoms.keyword": {"query": value, "boost": 8}
                    }
                }
            )

        if key == "min_date_naiss_dirigeant" and value is not None:
            min_date_naiss_dirigeant = value
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

        if key == "max_date_naiss_dirigeant" and value is not None:
            max_date_naiss_dirigeant = value
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
    # using a query (must and should) instead of a filter because filters do not give
    # a score which in turn does not boost certain documents over others
    search = search.query(
        "nested",
        path="dirigeants_pp",
        query=query.Bool(must=dirigeants_filters, should=boost_queries),
    )
    return search
