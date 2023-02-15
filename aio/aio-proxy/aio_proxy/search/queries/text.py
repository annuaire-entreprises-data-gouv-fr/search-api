def build_text_query(terms: str, matching_size: int):
    min_etab_ouverts_multiplier = {
        "field": "nombre_etablissements_ouverts",
        "factor": 1,
        "modifier": "log2p",
        "missing": 1,
    }
    mid_etab_ouverts_multiplier = {
        "field": "nombre_etablissements_ouverts",
        "factor": 10,
        "modifier": "log2p",
        "missing": 1,
    }
    max_etab_ouverts_multiplier = {
        "field": "nombre_etablissements_ouverts",
        "factor": 1000,
        "modifier": "log2p",
        "missing": 1,
    }

    text_query = {
        "bool": {
            "should": [
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "identifiant_association_unite_legale": {
                                    "query": terms,
                                    "boost": 50,
                                    "_name": "exact match identifiant association",
                                }
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "nom_complet.keyword": {
                                    "query": terms,
                                    "boost": 300,
                                    "_name": "exact nom_complet match",
                                }
                            }
                        },
                        "field_value_factor": max_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "nom_complet": {
                                    "query": terms,
                                    "operator": "AND",
                                    "boost": 50,
                                    "_name": "partial nom_complet match with AND",
                                }
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "sigle.keyword": {
                                    "query": terms,
                                    "boost": 100,
                                    "_name": "exact sigle match",
                                }
                            }
                        },
                        "field_value_factor": max_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "multi_match": {
                                "query": terms,
                                "fields": [
                                    "nom_raison_sociale",
                                    "denomination_usuelle_1",
                                    "denomination_usuelle_2",
                                    "denomination_usuelle_3",
                                    "sigle",
                                    "nom",
                                    "prenom",
                                ],
                                "type": "cross_fields",
                                "operator": "AND",
                                "_name": "match all champs denomination",
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "nested": {
                                "path": "etablissements",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "etablissements.enseigne_1. "
                                                    "keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact match "
                                                        "enseigne 1",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "etablissements.enseigne_1": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "enseigne 1",
                                                    }
                                                }
                                            },
                                            {
                                                "match_phrase": {
                                                    "etablissements.enseigne_2. "
                                                    "keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact match "
                                                        "enseigne 2",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "etablissements.enseigne_2": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "enseigne 2",
                                                    }
                                                }
                                            },
                                            {
                                                "match_phrase": {
                                                    "etablissements.enseigne_3."
                                                    "keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact "
                                                        "match enseigne 3",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "etablissements.enseigne_3": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "enseigne 3",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "etablissements.adresse": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "_name": "partial match "
                                                        "adresse",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "etablissements.nom_commercial": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "nom commercial",
                                                    }
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": terms,
                                                    "fields": [
                                                        "etablissements.nom_complet^15",
                                                        "etablissements.enseigne_1",
                                                        "etablissements.enseigne_2",
                                                        "etablissements.enseigne_3",
                                                        "etablissements.nom_commercial",
                                                        "etablissements.adresse",
                                                        "etablissements.commune",
                                                        "etablissements.concat_"
                                                        "enseigne_adresse_siren_siret",
                                                    ],
                                                    "type": "cross_fields",
                                                    "operator": "AND",
                                                    "_name": "match nom complet et "
                                                    "adresse",
                                                }
                                            },
                                        ],
                                    }
                                },
                                "inner_hits": {
                                    "size": matching_size,
                                    "sort": {
                                        "etablissements.etat_administratif": {
                                            "order": "asc"
                                        }
                                    },
                                },
                            }
                        },
                        "field_value_factor": min_etab_ouverts_multiplier,
                        "min_score": 4,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "liste_dirigeants": {
                                    "query": terms,
                                    "operator": "AND",
                                    "boost": 10,
                                    "_name": "partial match liste dirigeants",
                                }
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "liste_elus": {
                                    "query": terms,
                                    "operator": "AND",
                                    "boost": 10,
                                    "_name": "partial match liste élus",
                                }
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
            ],
        }
    }
    return text_query
