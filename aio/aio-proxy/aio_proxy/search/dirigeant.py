from elasticsearch_dsl import query


def search_dirigeant(search, **kwargs):
    dirigeants_filters = []
    boost_queries = []

    for key, value in kwargs.items():
        if key == "nom_dirigeant" and value is not None:
            for nom in value.split(" "):
                dirigeants_filters.append({"match": {"dirigeants_pp.nom": nom}})
            boost_queries.append(
                {
                    "match_phrase": {
                        "dirigeants_pp.nom.keyword": {"query": value, "boost": 8}
                    }
                }
            )

        if key == "prenoms_dirigeant" and value is not None:
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
    search = search.query(
        "nested",
        path="dirigeants_pp",
        query=query.Bool(must=dirigeants_filters, should=boost_queries),
    )
    return search
