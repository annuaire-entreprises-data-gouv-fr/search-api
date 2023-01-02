from aio_proxy.search.helpers.elastic_fields import get_elasticsearch_field_name


def build_etablissements_filters(**params):
    """Filter search by matching an id in an array of ids,
        e.g ids : "id_convention_collective",
                  "id_uai",
                  "id_finess",
                  "id_rge",

    The parameters concerned by this function are bool variables that have a
    `TRUE` value when they exist, and are not indexed (in elasticsearch) when the
    value is missing, which is equivalent to having a `FALSE` value.
    e.g "convention_collective_renseignee",
        "est_finess",
        "est_uai",
        "est_entrepreneur_spectacle",
        "est_rge",
    In order to keep the elasticsearch index light, when the value is present for
    these variables, we index `TRUE`, and when the value is missing (meaning it's
    False), we do not index the value `FALSE`, we simply leave it empty.
    Instead, we use this function to filter these values, based on whether a
    value was indexed.
    Having a value equals >> TRUE and not having an indexed value equals >> FALSE.
    We use the "exists" elasticsearch filter to implement it."""

    boolean_filters = [
        "est_rge",
        "est_finess",
        "est_uai",
        "convention_collective_renseignee",
    ]
    id_filters = ["id_finess", "id_rge", "id_uai", "id_convention_collective"]
    text_filters = ["departement", "code_postal", "commune"]

    terms_filters = []
    must_filters = []
    must_not_filters = []

    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in params.items():

        if param_value is not None and param_name in text_filters:
            terms_filters.append(
                {
                    "terms": {
                        "etablissements." + param_name: param_value,
                    }
                }
            )

        if param_value is not None and param_name in id_filters:
            field = get_elasticsearch_field_name(param_name)
            must_filters.append(
                {
                    "match": {
                        "etablissements."
                        + field: {
                            "query": param_value,
                            "_name": "Filter id:" + field,
                        }
                    }
                }
            )

        if param_value is not None and param_name in boolean_filters:
            field = get_elasticsearch_field_name(param_name)
            if param_value:
                must_filters.append({"exists": {"field": "etablissements." + field}})
            else:
                must_not_filters.append(
                    {"exists": {"field": "etablissements." + field}}
                )

    return terms_filters, must_filters, must_not_filters


def build_nested_etablissements_filters_query_with_inner_hits(**params):

    filters_query = {
        "nested": {
            "path": "etablissements",
            "query": {"bool": {}},
            "inner_hits": {},
        }
    }

    terms_filters, must_filters, must_not_filters = build_etablissements_filters(
        **params
    )

    if not (terms_filters or must_filters or must_not_filters):
        return None

    if terms_filters:
        filters_query["nested"]["query"]["bool"]["filter"] = terms_filters
    if must_filters:
        filters_query["nested"]["query"]["bool"]["must"] = must_filters
    if must_not_filters:
        filters_query["nested"]["query"]["bool"]["must_not"] = must_not_filters

    return filters_query


def build_nested_etablissements_filters_query_without_inner_hits(**params):

    filters_query = {
        "nested": {
            "path": "etablissements",
            "query": {"bool": {}},
        }
    }

    terms_filters, must_filters, must_not_filters = build_etablissements_filters(
        **params
    )

    if not (terms_filters or must_filters or must_not_filters):
        return None

    if terms_filters:
        filters_query["nested"]["query"]["bool"]["filter"] = terms_filters
    if must_filters:
        filters_query["nested"]["query"]["bool"]["must"] = must_filters
    if must_not_filters:
        filters_query["nested"]["query"]["bool"]["must_not"] = must_not_filters

    return filters_query


def add_nested_etablissements_filters_to_text_query(text_query, **params):
    terms_filters, must_filters, must_not_filters = build_etablissements_filters(
        **params
    )

    if terms_filters:
        text_query["bool"]["should"][3]["function_score"]["query"]["nested"]["query"][
            "bool"
        ]["filter"] = terms_filters
    if must_filters:
        text_query["bool"]["should"][3]["function_score"]["query"]["nested"]["query"][
            "bool"
        ]["must"] = must_filters
    if must_not_filters:
        text_query["bool"]["should"][3]["function_score"]["query"]["nested"]["query"][
            "bool"
        ]["must_not"] = must_not_filters
    return text_query