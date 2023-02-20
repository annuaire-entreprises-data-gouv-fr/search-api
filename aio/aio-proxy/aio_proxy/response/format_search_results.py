from aio_proxy.response.formatters.bool import format_bool_field
from aio_proxy.response.formatters.collectivite_territoriale import (
    format_collectivite_territoriale,
)
from aio_proxy.response.formatters.dirigeants import format_dirigeants
from aio_proxy.response.formatters.ess import format_ess
from aio_proxy.response.formatters.etablissements import (
    format_etablissements_list,
    format_siege,
)
from aio_proxy.response.helpers import format_nom_complet, get_value, is_dev_env


def format_search_results(results, include_etablissements=False):
    """Format API response to follow a specific schema."""
    formatted_results = []
    for result in results:

        def get_field(field, default=None):
            return get_value(result, field, default)

        result_formatted = {
            "siren": get_field("siren"),
            "nom_complet": format_nom_complet(
                get_field("nom_complet"),
                get_field("sigle"),
                get_field("denomination_usuelle_1_unite_legale"),
                get_field("denomination_usuelle_2_unite_legale"),
                get_field("denomination_usuelle_3_unite_legale"),
            ),
            "nom_raison_sociale": get_field("nom_raison_sociale"),
            "sigle": get_field("sigle"),
            "nombre_etablissements": int(get_field("nombre_etablissements", default=1)),
            "nombre_etablissements_ouverts": int(
                get_field("nombre_etablissements_ouverts", default=0)
            ),
            "siege": format_siege(get_field("siege")),
            "activite_principale": get_field("activite_principale_unite_legale"),
            "categorie_entreprise": get_field("categorie_entreprise"),
            "date_creation": get_field("date_creation_unite_legale"),
            "date_mise_a_jour": get_field("date_mise_a_jour_unite_legale"),
            "dirigeants": format_dirigeants(
                get_field("dirigeants_pp"), get_field("dirigeants_pm")
            ),
            "etat_administratif": get_field("etat_administratif_unite_legale"),
            "nature_juridique": get_field("nature_juridique_unite_legale"),
            "section_activite_principale": get_field("section_activite_principale"),
            "tranche_effectif_salarie": get_field(
                "tranche_effectif_salarie_unite_legale"
            ),
            "matching_etablissements": format_etablissements_list(
                get_field("matching_etablissements")
            ),
            "complements": {
                "collectivite_territoriale": format_collectivite_territoriale(
                    get_field("colter_code"),
                    get_field("colter_code_insee"),
                    get_field("colter_elus"),
                    get_field("colter_niveau"),
                ),
                "convention_collective_renseignee": get_field(
                    "convention_collective_renseignee"
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
                "est_finess": get_field("est_finess"),
                "est_rge": get_field("est_rge"),
                "est_service_public": get_field("est_service_public"),
                "est_uai": get_field("est_uai"),
                "identifiant_association": get_field(
                    "identifiant_association_unite_legale"
                ),
            },
        }

        # If 'include_etablissements' param is True, return 'etablissements' object
        # even if it's empty, otherwise do not return object
        if include_etablissements:
            etablissements = format_etablissements_list(get_field("etablissements"))
            result_formatted["etablissements"] = etablissements

        # Include score field for dev environment
        if is_dev_env():
            result_formatted["score"] = get_field("meta")
        formatted_results.append(result_formatted)
    return formatted_results
