def get_elasticsearch_field_name(param_name: str, search_unite_legale=False) -> str:
    # "est_bio", "est_finess", "est_rge", "est_organisme_formation" est_uai" and
    # "convention_collective_renseignee"
    # are special filters that are used to filter both `unite légale` and `établissements`
    # Consequently, the Elasticsearch fields used for these filters are different
    # when filtering on unité légale (where we use the same field names : "est_rge"
    # elastic field for "est_rge" filter),
    # and when filtering on établissements where we use the list fields (we use
    # "liste_rge" es field for "est_rge" filter).
    if search_unite_legale:
        corresponding_es_field = {
            "code_collectivite_territoriale": "colter_code",
            "est_association": "identifiant_association_unite_legale",
            "est_collectivite_territoriale": "colter_code",
        }
    else:
        corresponding_es_field = {
            "convention_collective_renseignee": "liste_idcc",
            "est_bio": "liste_id_bio",
            "est_finess": "liste_finess",
            "est_organisme_formation": "liste_id_organisme_formation",
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
