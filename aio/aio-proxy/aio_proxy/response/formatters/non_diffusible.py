def hide_non_diffusible_fields(result_formatted):
    hidden_fields = [
        "nom_complet",
        "nom_raison_sociale",
        "sigle",
    ]
    for field in hidden_fields:
        result_formatted[field] = "[NON-DIFFUSIBLE]"

    if result_formatted.get("siege"):
        result_formatted["siege"] = hide_non_diffusible_etablissement_fields(
            result_formatted["siege"]
        )

    if result_formatted.get("dirigeants"):
        result_formatted["dirigeants"] = hide_non_diffusible_dirigeants_fields(
            result_formatted["dirigeants"]
        )

    for matching_etablissement in result_formatted.get("matching_etablissements", []):
        hide_non_diffusible_etablissement_fields(matching_etablissement)

    for etablissement in result_formatted.get("etablissements", []):
        hide_non_diffusible_etablissement_fields(etablissement)

    return result_formatted


def hide_non_diffusible_dirigeants_fields(dirigeants):
    for dirigeant in dirigeants:
        if dirigeant["type_dirigeant"] == "personne physique":
            dirigeant["nom"] = "[NON-DIFFUSIBLE]"
            dirigeant["prenoms"] = "[NON-DIFFUSIBLE]"
            dirigeant["annee_de_naissance"] = "[NON-DIFFUSIBLE]"
    return dirigeants


def hide_non_diffusible_etablissement_fields(etablissement):
    # in order to keep `liste_enseignes` as an array of "NON-DIFFUSIBLE" strings
    if etablissement["liste_enseignes"]:
        etablissement["liste_enseignes"] = [
            "[NON-DIFFUSIBLE]" for enseigne in etablissement["liste_enseignes"]
        ]
    non_diffusible_fields = [
        "adresse",
        "cedex",
        "code_postal",
        "complement_adresse",
        "distribution_speciale",
        "indice_repetition",
        "libelle_cedex",
        "libelle_voie",
        "nom_commercial",
        "numero_voie",
        "type_voie",
    ]
    for field in non_diffusible_fields:
        etablissement[field] = "[NON-DIFFUSIBLE]"
    return etablissement
