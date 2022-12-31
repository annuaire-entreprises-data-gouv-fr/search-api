def get_elasticsearch_field_name(param_name: str) -> str:
    if param_name == "est_finess":
        return "liste_finess"
    elif param_name == "id_finess":
        return "liste_finess"
    elif param_name == "est_uai":
        return "liste_uai"
    elif param_name == "id_uai":
        return "liste_uai"
    elif param_name == "est_collectivite_territoriale":
        return "colter_code"
    elif param_name == "code_collectivite_territoriale":
        return "colter_code"
    elif param_name == "est_entrepreneur_spectacle":
        return "est_entrepreneur_spectacle"
    elif param_name == "est_rge":
        return "liste_rge"
    elif param_name == "id_rge":
        return "liste_rge"
    elif param_name == "convention_collective_renseignee":
        return "liste_idcc"
    elif param_name == "id_convention_collective":
        return "liste_idcc"
    elif param_name == "est_association":
        return "identifiant_association_unite_legale"
    else:
        return param_name
