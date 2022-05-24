from aio_proxy.helpers import set_default_to_none


def format_response(results):
    formatted_results = []
    for result in results:
        result_formatted = {
            "siren": set_default_to_none(result, "siren"),
            "siege": {
                "siret": set_default_to_none(result, "siret_siege"),
                "date_creation": set_default_to_none(result, "date_creation_siege"),
                "tranche_effectif_salarie": set_default_to_none(
                    result, "tranche_effectif_salarie_siege"),
                "date_debut_activite": set_default_to_none(result,
                                                           "date_debut_activite_siege"),
                "etat_adiministratif": set_default_to_none(result,
                                                           "etat_administratif_siege"),
                "activite_principale": set_default_to_none(result,
                                                           "activite_principale_siege"),
                "numero_voie": set_default_to_none(result, "numero_voie"),
                "type_voie": set_default_to_none(result, "type_voie"),
                "libelle_voie": set_default_to_none(result, "libelle_voie"),
                "code_postal": set_default_to_none(result, "code_postal"),
                "libelle_commune": set_default_to_none(result, "libelle_commune"),
                "indice_repetition": set_default_to_none(result, "indice_repetition"),
                "complement_adresse": set_default_to_none(result, "complement_adresse"),
                "commune": set_default_to_none(result, "commune"),
                "longitude": set_default_to_none(result, "longitude"),
                "latitude": set_default_to_none(result, "latitude"),
                "activite_principale_registre_metier": set_default_to_none(
                    result,  "activite_principale_registre_metier"),
            },
            "date_creation": set_default_to_none(result, "date_creation_unite_legale"),
            "tranche_effectif_salarie": set_default_to_none(
                result, "tranche_effectif_salarie_unite_legale"),
            "date_mise_a_jour": set_default_to_none(result,
                                                    "date_mise_a_jour_unite_legale"),
            "categorie_entreprise": set_default_to_none(result, "categorie_entreprise"),
            "etat_administratif": set_default_to_none(result,
                                                      "etat_administratif_unite_legale"),
            "nom_raison_sociale": set_default_to_none(result, "nom_raison_sociale"),
            "nature_juridique": set_default_to_none(result,
                                                    "nature_juridique_unite_legale"),
            "activite_principale": set_default_to_none(result,
                                                       "activite_principale_unite_legale"),
            "economie_sociale_solidaire": set_default_to_none(
                result, "economie_sociale_solidaire_unite_legale"
            ),
            "nom_complet": set_default_to_none(result, "nom_complet"),
            "nombre_etablissements": set_default_to_none(result,
                                                         "nombre_etablissements"),
            "nombre_etablissements_ouverts": set_default_to_none(
                result, "nombre_etablissements_ouverts"),
            "is_entrepreneur_individuel": set_default_to_none(result,
                                                              "is_entrepreneur_individuel")
        }
        formatted_results.append(result_formatted)
    return formatted_results
