def is_any_bilan_filter_used(search_params) -> bool:
    bilan_filters = [
        "ca_min",
        "ca_max",
        "resultat_net_min",
        "resultat_net_max",
    ]
    for param_name, param_value in search_params.dict().items():
        if param_value is not None and param_name in bilan_filters:
            return True
    return False
