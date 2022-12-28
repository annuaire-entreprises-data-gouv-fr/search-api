import os

from aio_proxy.response.helpers import (
    format_bool_field,
    format_collectivite_territoriale,
    format_dirigeants,
    format_ess,
    format_etablissements,
    format_siege,
    get_value,
)
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
            "siren": get_field("siren"),
            "nom_complet": get_field("nom_complet"),
            "nombre_etablissements": int(get_field("nombre_etablissements", default=1)),
            "nombre_etablissements_ouverts": int(
                get_field("nombre_etablissements_ouverts", default=0)
            ),
            "siege": format_siege(get_field("siege")),
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
            "dirigeants": format_dirigeants(
                get_field("dirigeants_pp"), get_field("dirigeants_pm")
            ),
            "etablissements": format_etablissements(get_field("etablissements")),
            "matched_etablissements": format_etablissements(
                get_field("inner_hits")
            ),
            "complements": {
                "collectivite_territoriale": format_collectivite_territoriale(
                    get_field("colter_code"),
                    get_field("colter_code_insee"),
                    get_field("colter_elus"),
                    get_field("colter_niveau"),
                ),
                "convention_collective_renseignee": format_bool_field(
                    get_field("liste_idcc"),
                ),
                "est_entrepreneur_individuel": get_field(
                    "est_entrepreneur_individuel", default=False
                ),
                "est_entrepreneur_spectacle": format_bool_field(
                    get_field("est_entrepreneur_spectacle")
                ),
                "est_ess": format_ess(
                    get_field("economie_sociale_solidaire_unite_legale")
                ),
                "est_finess": format_bool_field(get_field("liste_finess")),
                "est_rge": format_bool_field(get_field("liste_rge")),
                "est_uai": format_bool_field(get_field("liste_uai")),
                "identifiant_association": get_field(
                    "identifiant_association_unite_legale"
                ),
            },
        }
        # Include score field for dev environment
        if env == "dev":
            result_formatted["score"] = get_field("meta")
        formatted_results.append(result_formatted)
    return formatted_results
