def build_text_query(terms):
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
                        "field_value_factor": {
                            "field": "nombre_etablissements_ouverts",
                            "factor": 1,
                            "modifier": "log2p",
                            "missing": 1,
                        },
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "nom_complet.keyword": {
                                    "query": terms,
                                    "boost": 100,
                                    "_name": "exact nom_complet match",
                                }
                            }
                        },
                        "field_value_factor": {
                            "field": "nombre_etablissements_ouverts",
                            "factor": 1,
                            "modifier": "log2p",
                            "missing": 1,
                        },
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
                        "field_value_factor": {
                            "field": "nombre_etablissements_ouverts",
                            "factor": 1,
                            "modifier": "log2p",
                            "missing": 1,
                        },
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
                                                    "etablissements.enseigne_1.keyword":
                                                        {
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
                                                        "boost": 5,
                                                        "_name": "partial match "
                                                        "enseigne 1",
                                                    }
                                                }
                                            },
                                            {
                                                "match_phrase": {
                                                    "etablissements.enseigne_2.keyword":
                                                        {
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
                                                        "boost": 5,
                                                        "_name": "partial match "
                                                        "enseigne 2",
                                                    }
                                                }
                                            },
                                            {
                                                "match_phrase": {
                                                    "etablissements.enseigne_3.keyword":
                                                        {
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
                                                        "boost": 5,
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
                                                        "boost": 15,
                                                        "_name": "partial match "
                                                        "adresse",
                                                    }
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": terms,
                                                    "fields": [
                                                        "etablissements.nom_complet^15",
                                                        "etablissements.adresse",
                                                        "etablissements.concat_"
                                                        "enseigne_adresse_siren_siret",
                                                    ],
                                                    "type": "cross_fields",
                                                    "operator": "AND",
                                                    "_name": "match nom complet et "
                                                    "adresse",
                                                }
                                            },
                                        ]
                                    }
                                },
                                "inner_hits": {},
                            }
                        },
                        "field_value_factor": {
                            "field": "nombre_etablissements_ouverts",
                            "factor": 1,
                            "modifier": "log2p",
                            "missing": 1,
                        },
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
                        "field_value_factor": {
                            "field": "nombre_etablissements_ouverts",
                            "factor": 1,
                            "modifier": "log2p",
                            "missing": 1,
                        },
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
                        "field_value_factor": {
                            "field": "nombre_etablissements_ouverts",
                            "factor": 1,
                            "modifier": "log2p",
                            "missing": 1,
                        },
                    }
                },
            ],
        }
    }
    return text_query
