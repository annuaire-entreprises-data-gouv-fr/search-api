def hide_non_diffusible_fields(result_formatted):
    hidden_fields = [
        "nom_complet",
        "nom_raison_sociale",
        "sigle",
    ]
    for field in result_formatted.keys():
        if field in hidden_fields:
            result_formatted[field] = "[NON-DIFFUSIBLE]"
    return result_formatted
