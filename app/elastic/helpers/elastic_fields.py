def get_elasticsearch_field_name(param_name: str, search_unite_legale=False) -> str:
    # "est_bio", "est_finess", "est_rge", "est_uai" and
    # "convention_collective_renseignee"
    # are special filters that are used to filter both `unite légale` & `établissements`
    # Consequently, the Elasticsearch fields used for these filters are different
    # when filtering on unité légale (where we use the same field names : "est_rge"
    # elastic field for "est_rge" filter),
    # and when filtering on établissements where we use the list fields (we use
    # "liste_rge" es field for "est_rge" filter).
    if search_unite_legale:
        corresponding_es_field = {
            "bilan_renseigne": "unite_legale.bilan_financier.ca",
            "ca_min": "unite_legale.bilan_financier.ca",
            "ca_max": "unite_legale.bilan_financier.ca",
            "resultat_net_min": "unite_legale.bilan_financier.resultat_net",
            "resultat_net_max": "unite_legale.bilan_financier.resultat_net",
            "code_collectivite_territoriale": "unite_legale.colter_code",
            "est_collectivite_territoriale": "unite_legale.colter_code",
        }
    else:
        corresponding_es_field = {
            "convention_collective_renseignee": "liste_idcc",
            "est_bio": "liste_id_bio",
            "est_rge": "liste_rge",
            "est_uai": "liste_uai",
            "id_convention_collective": "liste_idcc",
            "id_finess": "liste_finess_geographique",
            "id_rge": "liste_rge",
            "id_uai": "liste_uai",
        }
    if param_name in corresponding_es_field:
        return corresponding_es_field[param_name]
    return f"unite_legale.{param_name}"
