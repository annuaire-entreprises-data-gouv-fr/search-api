from aio_proxy.response.helpers import get_value


def format_response(results):
    """Format API response to follow a specific schema."""
    formatted_results = []
    for result in results:

        def get_field(field, default=None):
            return get_value(result, field, default)

        result_formatted = {
            "siren": get_field("siren"),
            "siege": {
                "siret": get_field("siret_siege"),
                "date_creation": get_field("date_creation_siege"),
                "tranche_effectif_salarie": get_field("tranche_effectif_salarie_siege"),
                "date_debut_activite": get_field("date_debut_activite_siege"),
                "etat_adiministratif": get_field("etat_administratif_siege"),
                "activite_principale": get_field("activite_principale_siege"),
                "numero_voie": get_field("numero_voie"),
                "type_voie": get_field("type_voie"),
                "libelle_voie": get_field("libelle_voie"),
                "code_postal": get_field("code_postal"),
                "libelle_commune": get_field("libelle_commune"),
                "indice_repetition": get_field("indice_repetition"),
                "complement_adresse": get_field("complement_adresse"),
                "commune": get_field("commune"),
                "departement": get_field("departement"),
                "geo_id": get_field("geo_id"),
                "longitude": get_field("longitude"),
                "latitude": get_field("latitude"),
                "activite_principale_registre_metier": get_field(
                    "activite_principale_registre_metier"
                ),
            },
            "date_creation": get_field("date_creation_unite_legale"),
            "tranche_effectif_salarie": get_field(
                "tranche_effectif_salarie_unite_legale"
            ),
            "date_mise_a_jour": get_field("date_mise_a_jour_unite_legale"),
            "categorie_entreprise": get_field("categorie_entreprise"),
            "etat_administratif": get_field("etat_administratif_unite_legale"),
            "nom_raison_sociale": get_field("nom_raison_sociale"),
            "nature_juridique": get_field("nature_juridique_unite_legale"),
            "activite_principale": get_field("activite_principale_unite_legale"),
            "section_activite_principale": get_field("section_activite_principale"),
            "economie_sociale_solidaire": get_field(
                "economie_sociale_solidaire_unite_legale"
            ),
            "nom_complet": get_field("nom_complet"),
            "nombre_etablissements": int(get_field("nombre_etablissements", default=1)),
            "nombre_etablissements_ouverts": int(
                get_field("nombre_etablissements_ouverts", default=0)
            ),
            "is_entrepreneur_individuel": get_field(
                "is_entrepreneur_individuel", default="false"
            ).lower()
            == "true",
        }
        formatted_results.append(result_formatted)
    return formatted_results
