from app.elastic.queries.text import build_text_query

FONDATION_PATH = "fondation"
FONDATION_NUMERO_RNF = f"{FONDATION_PATH}.numero_rnf"

# Value of the `type_structure` list carried by every fondation document, whether
# it is an unité légale with a `numéro RNF` or a fondation without a SIRET.
FONDATION_STRUCTURE_TYPE = "fondation"


def build_fondation_text_query(terms: str):
    """We want to be able to search on fields located in the unité légale object.
    But fondations have their own fields that sometime conflict with unité légale.
    So the Fondation fields boosts outweigh the ones of the unité légale.
    This way a fondation whose `titre` matches has a better result than one matching
    on the unité légale.
    We also never return matching établissements when searching for fondations (inner hits size at 0).
    """
    return {
        "bool": {
            "should": [
                build_text_query(terms, matching_size=0),
                *build_fondation_fields_query(terms),
            ],
            "minimum_should_match": 1,
        }
    }


def build_fondation_fields_query(terms: str):
    return [
        {
            "term": {
                FONDATION_NUMERO_RNF: {
                    "value": terms.replace(" ", ""),
                    "boost": 1000,
                    "_name": "exact match numero rnf",
                }
            }
        },
        {
            "match_phrase": {
                f"{FONDATION_PATH}.titre": {
                    "query": terms,
                    "boost": 600,
                    "_name": "exact match titre",
                }
            }
        },
        {
            "match": {
                f"{FONDATION_PATH}.titre": {
                    "query": terms,
                    "operator": "and",
                    "boost": 100,
                    "_name": "all terms in titre",
                }
            }
        },
        {
            "match": {
                f"{FONDATION_PATH}.titre": {
                    "query": terms,
                    "operator": "and",
                    "fuzziness": "AUTO",
                    "boost": 30,
                    "_name": "fuzzy match titre",
                }
            }
        },
        {
            "match": {
                f"{FONDATION_PATH}.adresse": {
                    "query": terms,
                    "operator": "and",
                    "boost": 10,
                    "_name": "match adresse",
                }
            }
        },
        {
            "match": {
                f"{FONDATION_PATH}.ville": {
                    "query": terms,
                    "operator": "and",
                    "boost": 2,
                    "_name": "match ville",
                }
            }
        },
    ]
