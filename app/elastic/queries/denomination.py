def search_by_denomination_query(denomination: str):
    multiplier = "unite_legale.facteur_taille_entreprise"
    mid_multiplier = {
        "field": multiplier,
        "factor": 5,
        "modifier": "square",
        "missing": 0,
    }
    max_multiplier = {
        "field": multiplier,
        "factor": 10,
        "modifier": "square",
        "missing": 0,
    }
    denomination_query = {
        "bool": {
            "should": [
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "nom_complet.keyword": {
                                    "query": denomination,
                                    "boost": 100,
                                    "_name": "exact nom_complet match",
                                }
                            }
                        },
                        "field_value_factor": max_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "nom_complet": {
                                    "query": denomination,
                                    "operator": "AND",
                                    "boost": 50,
                                    "_name": "partial nom_complet match with AND",
                                }
                            }
                        },
                        "field_value_factor": max_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "unite_legale.sigle.keyword": {
                                    "query": denomination,
                                    "boost": 50,
                                    "_name": "exact sigle match",
                                }
                            }
                        },
                        "field_value_factor": mid_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "multi_match": {
                                "query": denomination,
                                "fields": [
                                    "unite_legale.nom_raison_sociale",
                                    "unite_legale.denomination_usuelle_1_unite_legale",
                                    "unite_legale.denomination_usuelle_2_unite_legale",
                                    "unite_legale.denomination_usuelle_3_unite_legale",
                                    "unite_legale.sigle",
                                    "unite_legale.nom",
                                    "unite_legale.prenom",
                                ],
                                "type": "cross_fields",
                                "operator": "AND",
                                "_name": "match all champs denomination",
                            }
                        },
                        "field_value_factor": mid_multiplier,
                    }
                },
            ],
        }
    }
    return denomination_query
