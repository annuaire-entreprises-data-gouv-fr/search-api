from elasticsearch_dsl import Q

from app.search.helpers.elastic_fields import get_elasticsearch_field_name


def filter_search_by_bool_fields_unite_legale(
    search,
    search_params,
    filters_to_include: list,
):
    for param_name, param_value in search_params.dict().items():
        should_apply_bool_filter = (
            param_value is not None and param_name in filters_to_include
        )
        if should_apply_bool_filter:
            # Check if bool filter value is True or False
            if param_value:
                search = search.filter(
                    "exists",
                    field=get_elasticsearch_field_name(
                        param_name, search_unite_legale=True
                    ),
                )
            else:
                search = search.filter(
                    "bool",
                    must_not=[
                        Q(
                            "exists",
                            field=get_elasticsearch_field_name(
                                param_name, search_unite_legale=True
                            ),
                        )
                    ],
                )
    return search


def filter_search_by_bool_nested_fields_unite_legale(
    search, search_params, filters_to_include: list, path
):
    for param_name, param_value in search_params.dict().items():
        should_apply_bool_filter = (
            param_value is not None and param_name in filters_to_include
        )
        if should_apply_bool_filter:
            # Check if bool filter value is True or False
            if param_value:
                search = search.filter(
                    "bool",
                    must=[
                        Q(
                            "nested",
                            path=path,
                            query=Q(
                                "exists",
                                field=get_elasticsearch_field_name(
                                    param_name, search_unite_legale=True
                                ),
                            ),
                        )
                    ],
                )
            else:
                search = search.filter(
                    "bool",
                    must_not=[
                        Q(
                            "nested",
                            path=path,
                            query=Q(
                                "exists",
                                field=get_elasticsearch_field_name(
                                    param_name, search_unite_legale=True
                                ),
                            ),
                        )
                    ],
                )
    return search
