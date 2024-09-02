def exclude_etablissements_from_search(es_search_builder):
    # By default, exclude etablissements list from response
    include_etablissements = (
        es_search_builder.search_params.include_admin
        and "ETABLISSEMENTS" in es_search_builder.search_params.include_admin
    )

    if not include_etablissements:
        es_search_builder.es_search_client = es_search_builder.es_search_client.source(
            excludes=["etablissements"]
        )
