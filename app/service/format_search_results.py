import json

from app.models.unite_legale import (
    UniteLegaleResponse,
)
from app.service.formatters.bilan_financier import format_bilan
from app.service.formatters.complements import format_complements
from app.service.formatters.dirigeants import format_dirigeants
from app.service.formatters.etablissements import (
    format_etablissements_list,
    format_siege,
)
from app.service.formatters.immatriculation import format_immatriculation
from app.service.formatters.nature_juridique import format_nature_juridique
from app.service.formatters.nom_complet import format_nom_complet
from app.service.formatters.non_diffusible import (
    hide_non_diffusible_fields,
)
from app.utils.helpers import (
    create_admin_fields_to_include,
    create_fields_to_include,
    get_value,
    is_dev_env,
)


def format_single_unite_legale(result, search_params):
    result_unite_legale = result["unite_legale"]

    def get_field(field, default=None):
        value = result_unite_legale.get(field, default)
        if value is None:
            return default
        return value

    unite_legale_fields = {
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
        "nombre_etablissements": int(get_field("nombre_etablissements", default=0)),
        "nombre_etablissements_ouverts": int(
            get_field("nombre_etablissements_ouverts", default=0)
        ),
        "activite_principale": get_field("activite_principale_unite_legale"),
        "categorie_entreprise": get_field("categorie_entreprise"),
        "caractere_employeur": get_field("caractere_employeur"),
        "annee_categorie_entreprise": get_field("annee_categorie_entreprise"),
        "date_creation": get_field("date_creation_unite_legale"),
        "date_fermeture": get_field("date_fermeture"),
        "date_mise_a_jour": get_field("date_mise_a_jour"),
        "date_mise_a_jour_insee": get_field("date_mise_a_jour_insee"),
        "date_mise_a_jour_rne": get_field("date_mise_a_jour_rne"),
        "etat_administratif": get_field("etat_administratif_unite_legale"),
        "nature_juridique": format_nature_juridique(
            get_field("nature_juridique_unite_legale")
        ),
        "section_activite_principale": get_field("section_activite_principale"),
        "tranche_effectif_salarie": get_field("tranche_effectif_salarie_unite_legale"),
        "annee_tranche_effectif_salarie": get_field("annee_tranche_effectif_salarie"),
        "statut_diffusion": get_field("statut_diffusion_unite_legale"),
    }
    formatted_unite_legale = UniteLegaleResponse(**unite_legale_fields)

    # Some search parameters control fields included in api response
    fields_to_include = create_fields_to_include(
        search_params
    ) + create_admin_fields_to_include(search_params)

    for field in fields_to_include:
        if field == "SIEGE":
            siege = format_siege(get_field("siege"))
            formatted_unite_legale.siege = siege
        elif field == "DIRIGEANTS":
            dirigeants = format_dirigeants(
                get_field("dirigeants_pp"),
                get_field("dirigeants_pm"),
            )
            formatted_unite_legale.dirigeants = dirigeants
        elif field == "FINANCES":
            finances = format_bilan(get_field("bilan_financier"))
            formatted_unite_legale.finances = finances
        elif field == "COMPLEMENTS":
            complements = format_complements(result_unite_legale)
            formatted_unite_legale.complements = complements
        elif field == "MATCHING_ETABLISSEMENTS":
            matching_etablissements = format_etablissements_list(
                get_value(result, "matching_etablissements")
            )
            formatted_unite_legale.matching_etablissements = matching_etablissements
        elif field == "SLUG":
            slug = get_field("slug")
            formatted_unite_legale.slug = slug
        elif field == "ETABLISSEMENTS":
            etablissements = format_etablissements_list(get_field("etablissements"))
            formatted_unite_legale.etablissements = etablissements
        elif field == "IMMATRICULATION":
            immatriculation = format_immatriculation(get_field("immatriculation"))
            formatted_unite_legale.immatriculation = immatriculation
        elif field == "SCORE":
            score = result.get("meta")["score"]
            formatted_unite_legale.score = score

    # Include search score and tree field for dev environment
    if is_dev_env():
        meta = result.get("meta")
        formatted_unite_legale.meta = json.loads(json.dumps(meta, default=str))

    # Hide most fields if unité légale is non-diffusible
    is_non_diffusible = (
        True
        if result_unite_legale.get("statut_diffusion_unite_legale") == "P"
        else False
    )
    if is_non_diffusible:
        formatted_unite_legale = hide_non_diffusible_fields(
            formatted_unite_legale.dict(exclude_unset=True)
        )
        return formatted_unite_legale

    # `exclude_unset`` option hides fields which were not
    # explicitly set when creating response object
    return formatted_unite_legale


def format_search_results(results, search_params):
    """Main formatting function for all results."""
    formatted_results = []
    for result in results:
        # If structure is unite légale
        if "unite_legale" in result:
            formatted_result = format_single_unite_legale(result, search_params)
            formatted_results.append(formatted_result)
    return formatted_results
