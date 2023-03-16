def is_any_etablissement_filter_used(**params) -> bool:
    etablissements_filters = [
        "commune",
        "code_postal",
        "convention_collective_renseignee",
        "departement",
        "est_bio",
        "est_finess",
        "est_organisme_formation",
        "est_uai",
        "est_rge",
        "id_convention_collective",
        "id_uai",
        "id_finess",
        "id_rge",
    ]
    for param_name, param_value in params.items():
        if param_value is not None and param_name in etablissements_filters:
            return True
    return False
