from app.elastic.helpers.elastic_fields import get_elasticsearch_field_name


def filter_term_search_unite_legale(
    search,
    search_params,
    filters_to_include: list,
):
    """Use filters to reduce search results."""
    # Fields where the boolean is derived from the existence of the field
    # (e.g. est_fondation is True when numero_rnf exists)
    EXISTS_BOOL_FIELDS = {"est_fondation"}

    for param_name, param_value in search_params.dict().items():
        if param_value is not None and param_name in filters_to_include:
            es_field_name = get_elasticsearch_field_name(
                param_name, search_unite_legale=True
            )

            if param_name in EXISTS_BOOL_FIELDS:
                if param_value:
                    search = search.filter("exists", field=es_field_name)
                else:
                    search = search.filter(
                        "bool", must_not=[{"exists": {"field": es_field_name}}]
                    )
            else:
                search = search.filter("term", **{es_field_name: param_value})

    return search


def filter_term_list_search_unite_legale(
    search, search_params, filters_to_include: list
):
    """Use filters to reduce search results."""
    # search_params is the object containing the list of parameters (filters) provided
    # in the request
    for param_name, param_value in search_params.dict().items():
        if param_value is not None and param_name in filters_to_include:
            search = search.filter(
                "terms",
                **{
                    get_elasticsearch_field_name(
                        param_name, search_unite_legale=True
                    ): param_value
                },
            )
    return search
