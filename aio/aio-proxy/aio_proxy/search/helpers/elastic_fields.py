def get_elasticsearch_field_name(param_name: str) -> str:
    corresponding_es_field = {
        "code_collectivite_territoriale": "colter_code",
        "convention_collective_renseignee": "liste_idcc",
        "est_association": "identifiant_association_unite_legale",
        "est_collectivite_territoriale": "colter_code",
        "est_finess": "liste_finess",
        "est_rge": "liste_rge",
        "est_uai": "liste_uai",
        "id_convention_collective": "liste_idcc",
        "id_finess": "liste_finess",
        "id_rge": "liste_rge",
        "id_uai": "liste_uai",
    }
    if param_name in corresponding_es_field:
        return corresponding_es_field[param_name]
    return param_name
