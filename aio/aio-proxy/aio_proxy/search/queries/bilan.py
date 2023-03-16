from aio_proxy.search.helpers.elastic_fields import get_elasticsearch_field_name
from elasticsearch_dsl import query


def search_bilan(
    search,
    bilan_filters_to_include,
    **params,
):
    search_options = []
    bilan_filters = []
    for filter in bilan_filters_to_include:
        filter_value = params.get(filter, None)
        if filter_value is not None:
            if "min" in filter:
                operator = "gte"
            if "max" in filter:
                operator = "lte"
            bilan_filters.append(
                {
                    "range": {
                        **{
                            get_elasticsearch_field_name(
                                filter, search_unite_legale=True
                            ): {operator: filter_value}
                        }
                    }
                }
            )

    if bilan_filters:
        search_options.append(
            query.Q(
                "nested",
                path="bilan_financier",
                query=query.Bool(must=bilan_filters),
            )
        )

    search = search.query("bool", should=search_options)
    return search
