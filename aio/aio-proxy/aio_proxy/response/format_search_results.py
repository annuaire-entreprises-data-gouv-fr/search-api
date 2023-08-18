import logging
from dataclasses import asdict, replace

from aio_proxy.response.formatters.bilan_financier import format_bilan
from aio_proxy.response.formatters.collectivite_territoriale import (
    format_collectivite_territoriale,
)
from aio_proxy.response.formatters.complements import format_complements
from aio_proxy.response.formatters.dirigeants import format_dirigeants
from aio_proxy.response.formatters.etablissements import (
    format_etablissements_list,
    format_siege,
)
from aio_proxy.response.formatters.insee_bool import format_insee_bool
from aio_proxy.response.formatters.non_diffusible import (
    hide_non_diffusible_fields,
)
from aio_proxy.response.formatters.selected_fields import (
    select_admin_fields,
    select_fields_to_include,
)
from aio_proxy.response.helpers import format_nom_complet, get_value, is_dev_env
from aio_proxy.response.unite_legale_model import (
    UniteLegaleResponse,
)


def format_single_unite_legale(result, search_params):
    unite_legale = result["unite_legale"]

    def get_field(field, default=None):
        return unite_legale.get(field, default)

    is_non_diffusible = (
        True if unite_legale.get("statut_diffusion_unite_legale") != "O" else False
    )

    formatted_unite_legale = UniteLegaleResponse(
        siren=get_field("siren"),
        nom_complet=format_nom_complet(
            get_field("nom_complet"),
            get_field("sigle"),
            get_field("denomination_usuelle_1_unite_legale"),
            get_field("denomination_usuelle_2_unite_legale"),
            get_field("denomination_usuelle_3_unite_legale"),
        ),
        nom_raison_sociale=get_field("nom_raison_sociale"),
        sigle=get_field("sigle"),
        nombre_etablissements=int(get_field("nombre_etablissements", default=1)),
        nombre_etablissements_ouverts=int(
            get_field("nombre_etablissements_ouverts", default=0)
        ),
        activite_principale=get_field("activite_principale_unite_legale"),
        categorie_entreprise=get_field("categorie_entreprise"),
        annee_categorie_entreprise=get_field("annee_categorie_entreprise"),
        date_creation=get_field("date_creation_unite_legale"),
        date_mise_a_jour=get_field("date_mise_a_jour_unite_legale"),
        etat_administratif=get_field("etat_administratif_unite_legale"),
        nature_juridique=get_field("nature_juridique_unite_legale"),
        section_activite_principale=get_field("section_activite_principale"),
        tranche_effectif_salarie=get_field("tranche_effectif_salarie_unite_legale"),
        annee_tranche_effectif_salarie=get_field("annee_tranche_effectif_salarie"),
        statut_diffusion=get_field("statut_diffusion_unite_legale"),
        matching_etablissements=format_etablissements_list(
            get_value(result, "matching_etablissements"), is_non_diffusible
        ),
    )

    if search_params.minimal:
        if search_params.include is None:
            return asdict(formatted_unite_legale)
        if "SIEGE" in search_params.include:
            siege = format_siege(get_field("siege"), is_non_diffusible)
            formatted_unite_legale = replace(formatted_unite_legale, siege=siege)
        if "DIRIGEANTS" in search_params.include:
            dirigeants = format_dirigeants(
                get_field("dirigeants_pp"),
                get_field("dirigeants_pm"),
                is_non_diffusible,
            )
            formatted_unite_legale = replace(
                formatted_unite_legale, dirigeants=dirigeants
            )
        if "FINANCES" in search_params.include:
            finances = format_bilan(get_field("bilan_financier"))
            formatted_unite_legale = replace(formatted_unite_legale, finances=finances)
        if "COMPLEMENTS" in search_params.include:
            complements = format_complements(
                collectivite_territoriale=format_collectivite_territoriale(
                    get_field("colter_code"),
                    get_field("colter_code_insee"),
                    get_field("colter_elus"),
                    get_field("colter_niveau"),
                ),
                convention_collective_renseignee=get_field(
                    "convention_collective_renseignee"
                ),
                egapro_renseignee=get_field("egapro_renseignee"),
                est_bio=get_field("est_bio"),
                est_entrepreneur_individuel=get_field(
                    "est_entrepreneur_individuel", default=False
                ),
                est_entrepreneur_spectacle=get_field("est_entrepreneur_spectacle"),
                est_ess=format_insee_bool(
                    get_field("economie_sociale_solidaire_unite_legale")
                ),
                est_finess=get_field("est_finess"),
                est_organisme_formation=get_field("est_organisme_formation"),
                est_qualiopi=get_field("est_qualiopi"),
                liste_id_organisme_formation=get_field("liste_id_organisme_formation"),
                est_rge=get_field("est_rge"),
                est_service_public=get_field("est_service_public"),
                est_societe_mission=format_insee_bool(get_field("est_societe_mission")),
                est_uai=get_field("est_uai"),
                identifiant_association=get_field(
                    "identifiant_association_unite_legale"
                ),
                statut_entrepreneur_spectacle=get_field(
                    "statut_entrepreneur_spectacle",
                ),
            )
            formatted_unite_legale = replace(
                formatted_unite_legale, complements=complements
            )
    if search_params.include_admin:
        if "etablissements" in search_params.include_admin:
            etablissements = format_etablissements_list(
                get_field("etablissements"), is_non_diffusible
            )
            formatted_unite_legale = replace(
                formatted_unite_legale, etablissements=etablissements
            )
        if "score" in search_params.include_admin:
            score = result.get("meta")["score"]
            formatted_unite_legale = replace(formatted_unite_legale, score=score)
        if "slug" in search_params.include_admin:
            slug = get_field("slug")
            formatted_unite_legale = replace(formatted_unite_legale, slug=slug)

    # Include search score and tree field for dev environment
    if is_dev_env():
        meta = result.get("meta")
        formatted_unite_legale = replace(formatted_unite_legale, meta=meta)

    # Hide most fields if unité légale is non-diffusible
    if is_non_diffusible:
        formatted_unite_legale = hide_non_diffusible_fields(
            asdict(formatted_unite_legale)
        )
        return formatted_unite_legale

    return asdict(formatted_unite_legale)


# Main formatting function for all results
def format_search_results(results, search_params):
    """Format API response to follow a specific schema."""
    formatted_results = []
    for result in results:
        logging.info(f"%%%%%%%%%%%%%%%{result}")
        if "unite_legale" in result:
            formatted_result = format_single_unite_legale(result, search_params)
            formatted_results.append(formatted_result)
    return formatted_results


def format(results, search_params):
    formatted_results = []
    for result in results:

        def get_field(field, default=None):
            return get_value(result["unite_legale"], field, default)

        # Hide some fields if non-diffusible
        is_non_diffusible = (
            True if get_field("statut_diffusion_unite_legale") != "O" else False
        )

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
            "siege": format_siege(get_field("siege"), is_non_diffusible),
            "activite_principale": get_field("activite_principale_unite_legale"),
            "categorie_entreprise": get_field("categorie_entreprise"),
            "annee_categorie_entreprise": get_field("annee_categorie_entreprise"),
            "date_creation": get_field("date_creation_unite_legale"),
            "date_mise_a_jour": get_field("date_mise_a_jour_unite_legale"),
            "dirigeants": format_dirigeants(
                get_field("dirigeants_pp"),
                get_field("dirigeants_pm"),
                is_non_diffusible,
            ),
            "etat_administratif": get_field("etat_administratif_unite_legale"),
            "nature_juridique": get_field("nature_juridique_unite_legale"),
            "section_activite_principale": get_field("section_activite_principale"),
            "tranche_effectif_salarie": get_field(
                "tranche_effectif_salarie_unite_legale"
            ),
            "annee_tranche_effectif_salarie": get_field(
                "annee_tranche_effectif_salarie"
            ),
            "statut_diffusion": get_field("statut_diffusion_unite_legale"),
            "matching_etablissements": format_etablissements_list(
                get_value(result, "matching_etablissements"), is_non_diffusible
            ),
            "finances": format_bilan(get_field("bilan_financier")),
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
                "egapro_renseignee": get_field("egapro_renseignee"),
                "est_bio": get_field("est_bio"),
                "est_entrepreneur_individuel": get_field(
                    "est_entrepreneur_individuel", default=False
                ),
                "est_entrepreneur_spectacle": get_field("est_entrepreneur_spectacle"),
                "est_ess": format_insee_bool(
                    get_field("economie_sociale_solidaire_unite_legale")
                ),
                "est_finess": get_field("est_finess"),
                "est_organisme_formation": get_field("est_organisme_formation"),
                "est_qualiopi": get_field("est_qualiopi"),
                "liste_id_organisme_formation": get_field(
                    "liste_id_organisme_formation"
                ),
                "est_rge": get_field("est_rge"),
                "est_service_public": get_field("est_service_public"),
                "est_societe_mission": format_insee_bool(
                    get_field("est_societe_mission")
                ),
                "est_uai": get_field("est_uai"),
                "identifiant_association": get_field(
                    "identifiant_association_unite_legale"
                ),
                "statut_entrepreneur_spectacle": get_field(
                    "statut_entrepreneur_spectacle",
                ),
            },
        }

        # Select fields to return
        if search_params.minimal:
            select_fields_to_include(search_params.include, result_formatted)

        if search_params.include_admin:
            etablissements = format_etablissements_list(
                get_field("etablissements"), is_non_diffusible
            )
            score = get_value(result, "meta")["score"]
            slug = get_field("slug")
            select_admin_fields(
                search_params.include_admin,
                etablissements,
                score,
                slug,
                result_formatted,
            )

        # Hide most fields if unité légale is non-diffusible
        if is_non_diffusible:
            result_formatted = hide_non_diffusible_fields(result_formatted)

        # Include search score and tree field for dev environment
        if is_dev_env():
            result_formatted["meta"] = get_value(result, "meta")
        formatted_results.append(result_formatted)
    return formatted_results
