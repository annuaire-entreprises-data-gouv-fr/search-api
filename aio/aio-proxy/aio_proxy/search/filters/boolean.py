from aio_proxy.search.helpers.elastic_fields import get_elasticsearch_field_name
from elasticsearch_dsl import Q


def filter_search_by_bool_fields_unite_legale(
    search, filters_to_include: list, **params
):
    for param_name, param_value in params.items():
        should_apply_bool_filter = (
            param_value is not None and param_name in filters_to_include
        )
        if should_apply_bool_filter:
            # Check if bool filter value is True or False
            if param_value:
                search = search.filter(
                    "exists", field=get_elasticsearch_field_name(param_name)
                )
            else:
                search = search.filter(
                    "bool",
                    must_not=[
                        Q("exists", field=get_elasticsearch_field_name(param_name))
                    ],
                )
    return search
