def build_text_query(terms: str, matching_size: int, sort_by_size: bool = False):
    if sort_by_size:
        return sort_by_size_text_query(terms, matching_size)
    else:
        return sort_by_nombre_etablissement_query(terms, matching_size)


def sort_by_size_text_query(terms: str, matching_size: int):
    multiplier = "unite_legale.facteur_taille_entreprise"
    min_multiplier = {
        "field": multiplier,
        "factor": 1,
        "modifier": "log2p",
        "missing": 0,
    }
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
    text_query = {
        "bool": {
            "should": [
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "unite_legale.identifiant_association_unite_legale": {
                                    "query": terms,
                                    "boost": 50,
                                    "_name": "exact match identifiant association",
                                }
                            }
                        },
                        "field_value_factor": mid_multiplier,
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
                        "field_value_factor": max_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            # dis_max keeps only the best clause: exact words
                            # (unstemmed) score as before, stemmed-only matches
                            # (e.g. "PARISSE" -> "PARIS") score lower.
                            "dis_max": {
                                "queries": [
                                    {
                                        "match": {
                                            "nom_complet.exact": {
                                                "query": terms,
                                                "operator": "AND",
                                                "boost": 50,
                                                "_name": "partial nom_complet exact words match",
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "nom_complet": {
                                                "query": terms,
                                                "operator": "AND",
                                                "boost": 15,
                                                "_name": "partial nom_complet match with AND",
                                            }
                                        }
                                    },
                                ]
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
                                    "query": terms,
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
                                "query": terms,
                                "fields": [
                                    "unite_legale.nom_raison_sociale",
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
                {
                    "function_score": {
                        "query": {
                            "nested": {
                                "path": "unite_legale.etablissements",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "unite_legale.etablissements."
                                                    "enseigne_1.keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact match "
                                                        "enseigne 1",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements."
                                                    "enseigne_1": {
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
                                                    "unite_legale.etablissements."
                                                    "enseigne_2.keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact match "
                                                        "enseigne 2",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements."
                                                    "enseigne_2": {
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
                                                    "unite_legale.etablissements.enseigne_3."
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
                                                    "unite_legale.etablissements."
                                                    "enseigne_3": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "enseigne 3",
                                                    }
                                                }
                                            },
                                            {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "match": {
                                                                "unite_legale.etablissements."
                                                                "adresse": {
                                                                    "query": terms,
                                                                    "operator": "AND",
                                                                    "_name": "partial match "
                                                                    "adresse",
                                                                }
                                                            }
                                                        }
                                                    ],
                                                    "must_not": [
                                                        {
                                                            "term": {
                                                                "unite_legale.etablissements.est_protege_legacy": True
                                                            }
                                                        }
                                                    ],
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements."
                                                    "nom_commercial": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "nom commercial",
                                                    }
                                                }
                                            },
                                            {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "multi_match": {
                                                                "query": terms,
                                                                "fields": [
                                                                    "unite_legale.etablissements.nom_complet^15",
                                                                    "unite_legale.etablissements.enseigne_1",
                                                                    "unite_legale.etablissements.enseigne_2",
                                                                    "unite_legale.etablissements.enseigne_3",
                                                                    "unite_legale.etablissements.nom_commercial",
                                                                    "unite_legale.etablissements.sigle",
                                                                    "unite_legale.etablissements.adresse",
                                                                    "unite_legale.etablissements.commune",
                                                                    "unite_legale.etablissements.concat_unite_legale.enseigne_adresse_siren_siret",
                                                                ],
                                                                "type": "cross_fields",
                                                                "operator": "AND",
                                                                "_name": "match nom complet et adresse",
                                                            }
                                                        }
                                                    ],
                                                    "must_not": [
                                                        {
                                                            "term": {
                                                                "unite_legale.etablissements.est_protege_legacy": True
                                                            }
                                                        }
                                                    ],
                                                }
                                            },
                                            # Same match without the address fields for protected legacy,
                                            # commune stays public so it is kept
                                            {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "multi_match": {
                                                                "query": terms,
                                                                "fields": [
                                                                    "unite_legale.etablissements.nom_complet^15",
                                                                    "unite_legale.etablissements.enseigne_1",
                                                                    "unite_legale.etablissements.enseigne_2",
                                                                    "unite_legale.etablissements.enseigne_3",
                                                                    "unite_legale.etablissements.nom_commercial",
                                                                    "unite_legale.etablissements.sigle",
                                                                    "unite_legale.etablissements.commune",
                                                                ],
                                                                "type": "cross_fields",
                                                                "operator": "AND",
                                                                "_name": "match nom complet et adresse",
                                                            }
                                                        }
                                                    ],
                                                    "filter": [
                                                        {
                                                            "term": {
                                                                "unite_legale.etablissements.est_protege_legacy": True
                                                            }
                                                        }
                                                    ],
                                                }
                                            },
                                        ],
                                    }
                                },
                                "inner_hits": {
                                    "size": matching_size,
                                    "sort": {
                                        "unite_legale.etablissements."
                                        "etat_administratif": {"order": "asc"}
                                    },
                                },
                            }
                        },
                        "field_value_factor": min_multiplier,
                        "min_score": 4,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        # Same dis_max logic as nom_complet.
                                        "dis_max": {
                                            "queries": [
                                                {
                                                    "match": {
                                                        "unite_legale.liste_dirigeants.exact": {
                                                            "query": terms,
                                                            "operator": "AND",
                                                            "boost": 30,
                                                            "_name": "exact words match liste dirigeants",
                                                        }
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "unite_legale.liste_dirigeants": {
                                                            "query": terms,
                                                            "operator": "AND",
                                                            "boost": 10,
                                                            "_name": "partial match liste dirigeants",
                                                        }
                                                    }
                                                },
                                            ]
                                        }
                                    }
                                ],
                                "filter": [
                                    {
                                        # Privacy rule:
                                        # we allow searching `liste_dirigeants` only when diffusion
                                        # is NOT "P". Without this, a document could match purely
                                        # because of dirigeants data even when diffusion is "P".
                                        "bool": {
                                            "must_not": [
                                                {
                                                    "term": {
                                                        "unite_legale.statut_diffusion_unite_legale": "P"
                                                    }
                                                },
                                            ]
                                        }
                                    }
                                ],
                            }
                        },
                        "field_value_factor": min_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "multi_match": {
                                "query": terms,
                                "fields": [
                                    "unite_legale.nom_raison_sociale",
                                    "unite_legale.sigle",
                                    "unite_legale.nom",
                                    "unite_legale.prenom",
                                    "unite_legale.liste_dirigeants",
                                ],
                                "type": "cross_fields",
                                "operator": "AND",
                                "_name": "match denomination et dirigeants",
                            }
                        },
                        "field_value_factor": mid_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "unite_legale.liste_elus": {
                                    "query": terms,
                                    "operator": "AND",
                                    "boost": 10,
                                    "_name": "partial match liste élus",
                                }
                            }
                        },
                        "field_value_factor": min_multiplier,
                    }
                },
            ],
        }
    }
    return text_query


def sort_by_nombre_etablissement_query(terms: str, matching_size: int):
    multiplier = "unite_legale.nombre_etablissements_ouverts"
    min_multiplier = {
        "field": multiplier,
        "factor": 1,
        "modifier": "log2p",
        "missing": 1,
    }
    mid_multiplier = {
        "field": multiplier,
        "factor": 10,
        "modifier": "log2p",
        "missing": 1,
    }
    max_multiplier = {
        "field": multiplier,
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
                                "unite_legale.identifiant_association_unite_legale": {
                                    "query": terms,
                                    "boost": 50,
                                    "_name": "exact match identifiant association",
                                }
                            }
                        },
                        "field_value_factor": mid_multiplier,
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
                        "field_value_factor": max_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            # dis_max keeps only the best clause: exact words
                            # (unstemmed) score as before, stemmed-only matches
                            # (e.g. "PARISSE" -> "PARIS") score lower.
                            "dis_max": {
                                "queries": [
                                    {
                                        "match": {
                                            "nom_complet.exact": {
                                                "query": terms,
                                                "operator": "AND",
                                                "boost": 50,
                                                "_name": "partial nom_complet exact words match",
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "nom_complet": {
                                                "query": terms,
                                                "operator": "AND",
                                                "boost": 15,
                                                "_name": "partial nom_complet match with AND",
                                            }
                                        }
                                    },
                                ]
                            }
                        },
                        "field_value_factor": mid_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "unite_legale.sigle.keyword": {
                                    "query": terms,
                                    "boost": 100,
                                    "_name": "exact sigle match",
                                }
                            }
                        },
                        "field_value_factor": max_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "multi_match": {
                                "query": terms,
                                "fields": [
                                    "unite_legale.nom_raison_sociale",
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
                {
                    "function_score": {
                        "query": {
                            "nested": {
                                "path": "unite_legale.etablissements",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "unite_legale.etablissements."
                                                    "enseigne_1.keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact match "
                                                        "enseigne 1",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements."
                                                    "enseigne_1": {
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
                                                    "unite_legale.etablissements."
                                                    "enseigne_2.keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact match "
                                                        "enseigne 2",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements."
                                                    "enseigne_2": {
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
                                                    "unite_legale.etablissements.enseigne_3."
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
                                                    "unite_legale.etablissements."
                                                    "enseigne_3": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "enseigne 3",
                                                    }
                                                }
                                            },
                                            {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "match": {
                                                                "unite_legale.etablissements."
                                                                "adresse": {
                                                                    "query": terms,
                                                                    "operator": "AND",
                                                                    "_name": "partial match adresse",
                                                                }
                                                            }
                                                        }
                                                    ],
                                                    "must_not": [
                                                        {
                                                            "term": {
                                                                "unite_legale.etablissements.est_protege_legacy": True
                                                            }
                                                        }
                                                    ],
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements."
                                                    "nom_commercial": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "nom commercial",
                                                    }
                                                }
                                            },
                                            {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "multi_match": {
                                                                "query": terms,
                                                                "fields": [
                                                                    "unite_legale.etablissements.nom_complet^15",
                                                                    "unite_legale.etablissements.enseigne_1",
                                                                    "unite_legale.etablissements.enseigne_2",
                                                                    "unite_legale.etablissements.enseigne_3",
                                                                    "unite_legale.etablissements.nom_commercial",
                                                                    "unite_legale.etablissements.sigle",
                                                                    "unite_legale.etablissements.adresse",
                                                                    "unite_legale.etablissements.commune",
                                                                    "unite_legale.etablissements.concat_unite_legale.enseigne_adresse_siren_siret",
                                                                ],
                                                                "type": "cross_fields",
                                                                "operator": "AND",
                                                                "_name": "match nom complet et adresse",
                                                            }
                                                        }
                                                    ],
                                                    "must_not": [
                                                        {
                                                            "term": {
                                                                "unite_legale.etablissements.est_protege_legacy": True
                                                            }
                                                        }
                                                    ],
                                                }
                                            },
                                            # Same match without the address fields for protected legacy SIREN,
                                            # commune stays public so it is kept
                                            {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "multi_match": {
                                                                "query": terms,
                                                                "fields": [
                                                                    "unite_legale.etablissements.nom_complet^15",
                                                                    "unite_legale.etablissements.enseigne_1",
                                                                    "unite_legale.etablissements.enseigne_2",
                                                                    "unite_legale.etablissements.enseigne_3",
                                                                    "unite_legale.etablissements.nom_commercial",
                                                                    "unite_legale.etablissements.sigle",
                                                                    "unite_legale.etablissements.commune",
                                                                ],
                                                                "type": "cross_fields",
                                                                "operator": "AND",
                                                                "_name": "match nom complet et adresse",
                                                            }
                                                        }
                                                    ],
                                                    "filter": [
                                                        {
                                                            "term": {
                                                                "unite_legale.etablissements.est_protege_legacy": True
                                                            }
                                                        }
                                                    ],
                                                }
                                            },
                                        ],
                                    }
                                },
                                "inner_hits": {
                                    "size": matching_size,
                                    "sort": {
                                        "unite_legale.etablissements."
                                        "etat_administratif": {"order": "asc"}
                                    },
                                },
                            }
                        },
                        "field_value_factor": min_multiplier,
                        "min_score": 2,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        # Same dis_max logic as nom_complet.
                                        "dis_max": {
                                            "queries": [
                                                {
                                                    "match": {
                                                        "unite_legale.liste_dirigeants.exact": {
                                                            "query": terms,
                                                            "operator": "AND",
                                                            "boost": 30,
                                                            "_name": "exact words match liste dirigeants",
                                                        }
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "unite_legale.liste_dirigeants": {
                                                            "query": terms,
                                                            "operator": "AND",
                                                            "boost": 10,
                                                            "_name": "partial match liste dirigeants",
                                                        }
                                                    }
                                                },
                                            ]
                                        }
                                    }
                                ],
                                "filter": [
                                    {
                                        # Same gating as above (different scoring/multiplier branch).
                                        "bool": {
                                            "must_not": [
                                                {
                                                    "term": {
                                                        "unite_legale.statut_diffusion_unite_legale": "P"
                                                    }
                                                },
                                            ]
                                        }
                                    }
                                ],
                            }
                        },
                        "field_value_factor": mid_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "multi_match": {
                                "query": terms,
                                "fields": [
                                    "unite_legale.nom_raison_sociale",
                                    "unite_legale.sigle",
                                    "unite_legale.nom",
                                    "unite_legale.prenom",
                                    "unite_legale.liste_dirigeants",
                                ],
                                "type": "cross_fields",
                                "operator": "AND",
                                "_name": "match denomination et dirigeants",
                            }
                        },
                        "field_value_factor": mid_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "unite_legale.liste_elus": {
                                    "query": terms,
                                    "operator": "AND",
                                    "boost": 10,
                                    "_name": "partial match liste élus",
                                }
                            }
                        },
                        "field_value_factor": mid_multiplier,
                    }
                },
            ],
        }
    }
    return text_query
