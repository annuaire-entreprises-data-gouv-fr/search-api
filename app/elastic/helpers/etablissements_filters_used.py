def is_any_etablissement_filter_used(search_params) -> bool:
    etablissements_filters = [
        "commune",
        "code_postal",
        "convention_collective_renseignee",
        "departement",
        "epci",
        "est_bio",
        "est_organisme_formation",
        "est_uai",
        "est_rge",
        "id_convention_collective",
        "id_uai",
        "id_rge",
        "region",
    ]
    for param_name, param_value in search_params.dict().items():
        if param_value is not None and param_name in etablissements_filters:
            return True
    return False
