from aio_proxy.response.helpers import get_value, format_dirigeants
import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV")


def format_response(results):
    """Format API response to follow a specific schema."""
    formatted_results = []
    for result in results:

        def get_field(field, default=None):
            return get_value(result, field, default)

        result_formatted = {
            "score": get_field("meta"),
            "siren": get_field("siren"),
            "siege": {
                "siret": get_field("siret_siege"),
                "date_creation": get_field("date_creation_siege"),
                "tranche_effectif_salarie": get_field("tranche_effectif_salarie_siege"),
                "date_debut_activite": get_field("date_debut_activite_siege"),
                "etat_administratif": get_field("etat_administratif_siege"),
                "activite_principale": get_field("activite_principale_siege"),
                "complement_adresse": get_field("complement_adresse"),
                "numero_voie": get_field("numero_voie"),
                "indice_repetition": get_field("indice_repetition"),
                "type_voie": get_field("type_voie"),
                "libelle_voie": get_field("libelle_voie"),
                "distribution_speciale": get_field("distribution_speciale"),
                "cedex": get_field("cedex"),
                "libelle_cedex": get_field("libelle_cedex"),
                "commune": get_field("commune"),
                "libelle_commune": get_field("libelle_commune"),
                "code_pays_etranger": get_field("code_pays_etranger"),
                "libelle_commune_etranger": get_field("libelle_commune_etranger"),
                "libelle_pays_etranger": get_field("libelle_pays_etranger"),
                "adresse_complete": get_field("adresse_etablissement"),
                "adresse_complete_secondaire": get_field("adresse_etablissement_2"),
                "code_postal": get_field("code_postal"),
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
            "dirigeants": format_dirigeants(
                get_field("dirigeants_pp"), get_field("dirigeants_pm")
            ),
        }
        # Hide score field for non dev environments
        if env != "dev":
            result_formatted.pop("score", None)
        formatted_results.append(result_formatted)
    return formatted_results
