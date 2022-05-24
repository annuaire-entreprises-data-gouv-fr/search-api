import json

from aio_proxy.response.helpers import set_default


def format_response(results):
    """Format API response to follow a specific schema."""
    formatted_results = []
    for result in results:
        result_formatted = {
            "siren": set_default(result, "siren"),
            "siege": {
                "siret": set_default(result, "siret_siege"),
                "date_creation": set_default(result, "date_creation_siege"),
                "tranche_effectif_salarie": set_default(
                    result, "tranche_effectif_salarie_siege"
                ),
                "date_debut_activite": set_default(result, "date_debut_activite_siege"),
                "etat_adiministratif": set_default(result, "etat_administratif_siege"),
                "activite_principale": set_default(result, "activite_principale_siege"),
                "numero_voie": set_default(result, "numero_voie"),
                "type_voie": set_default(result, "type_voie"),
                "libelle_voie": set_default(result, "libelle_voie"),
                "code_postal": set_default(result, "code_postal"),
                "libelle_commune": set_default(result, "libelle_commune"),
                "indice_repetition": set_default(result, "indice_repetition"),
                "complement_adresse": set_default(result, "complement_adresse"),
                "commune": set_default(result, "commune"),
                "longitude": set_default(result, "longitude"),
                "latitude": set_default(result, "latitude"),
                "activite_principale_registre_metier": set_default(
                    result, "activite_principale_registre_metier"
                ),
            },
            "date_creation": set_default(result, "date_creation_unite_legale"),
            "tranche_effectif_salarie": set_default(
                result, "tranche_effectif_salarie_unite_legale"
            ),
            "date_mise_a_jour": set_default(result, "date_mise_a_jour_unite_legale"),
            "categorie_entreprise": set_default(result, "categorie_entreprise"),
            "etat_administratif": set_default(
                result, "etat_administratif_unite_legale"
            ),
            "nom_raison_sociale": set_default(result, "nom_raison_sociale"),
            "nature_juridique": set_default(result, "nature_juridique_unite_legale"),
            "activite_principale": set_default(
                result, "activite_principale_unite_legale"
            ),
            "economie_sociale_solidaire": set_default(
                result, "economie_sociale_solidaire_unite_legale"
            ),
            "nom_complet": set_default(result, "nom_complet"),
            "nombre_etablissements": int(
                set_default(result, "nombre_etablissements", default=1)
            ),
            "nombre_etablissements_ouverts": int(
                set_default(result, "nombre_etablissements_ouverts", default=0)
            ),
            "is_entrepreneur_individuel": json.loads(
                set_default(
                    result, "is_entrepreneur_individuel", default="false"
                ).lower()
            ),
        }
        formatted_results.append(result_formatted)
    return formatted_results
