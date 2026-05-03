import json

from app.models.unite_legale import (
    UniteLegaleResponse,
)
from app.service.formatters.bilan_financier import format_bilan
from app.service.formatters.bodacc import format_bodacc
from app.service.formatters.complements import format_complements
from app.service.formatters.dirigeants import format_dirigeants
from app.service.formatters.etablissements import (
    format_etablissements_list,
    format_siege,
)
from app.service.formatters.immatriculation import format_immatriculation
from app.service.formatters.nature_juridique import format_nature_juridique
from app.service.formatters.nom_complet import format_nom_complet, get_nom_commercial
from app.service.formatters.non_diffusible import (
    mask_unite_legale,
)
from app.utils.helpers import (
    create_admin_fields_to_include,
    create_fields_to_include,
    get_value,
    is_dev_env,
)

# -------------------------
# Helpers
# -------------------------

def is_unite_legale_non_diffusible(data):
    return data.get("statut_diffusion_unite_legale") == "P"


# -------------------------
# Base builder
# -------------------------


def build_unite_legale_base(data):
    is_nd = is_unite_legale_non_diffusible(data)

    fields = {
        "siren": get_value(data, "siren"),
        "nom_complet": format_nom_complet(
            get_value(data, "nom_complet"),
            get_value(data, "sigle"),
            get_nom_commercial(get_value(data, "siege")),
            get_value(data, "est_personne_morale_insee"),
            is_nd,
        ),
        "nom_raison_sociale": get_value(data, "nom_raison_sociale"),
        "sigle": get_value(data, "sigle"),
        "nombre_etablissements": int(get_value(data, "nombre_etablissements", 0)),
        "nombre_etablissements_ouverts": int(
            get_value(data, "nombre_etablissements_ouverts", 0)
        ),
        "activite_principale": get_value(data, "activite_principale_unite_legale"),
        "activite_principale_naf25": get_value(
            data, "activite_principale_naf25_unite_legale"
        ),
        "categorie_entreprise": get_value(data, "categorie_entreprise"),
        "caractere_employeur": get_value(data, "caractere_employeur"),
        "annee_categorie_entreprise": get_value(data, "annee_categorie_entreprise"),
        "date_creation": get_value(data, "date_creation_unite_legale"),
        "date_fermeture": get_value(data, "date_fermeture"),
        "date_mise_a_jour": get_value(data, "date_mise_a_jour"),
        "date_mise_a_jour_insee": get_value(data, "date_mise_a_jour_insee"),
        "date_mise_a_jour_rne": get_value(data, "date_mise_a_jour_rne"),
        "etat_administratif": get_value(data, "etat_administratif_unite_legale"),
        "nature_juridique": format_nature_juridique(
            get_value(data, "nature_juridique_unite_legale")
        ),
        "section_activite_principale": get_value(data, "section_activite_principale"),
        "tranche_effectif_salarie": get_value(
            data, "tranche_effectif_salarie_unite_legale"
        ),
        "annee_tranche_effectif_salarie": get_value(
            data, "annee_tranche_effectif_salarie"
        ),
        "statut_diffusion": get_value(data, "statut_diffusion_unite_legale"),
    }

    return UniteLegaleResponse(**fields)


# -------------------------
# Field enrichment (dispatch map)
# -------------------------


def enrich_unite_legale(ul, search_result, raw_ul, fields_to_include):
    handlers = {
        "SIEGE": lambda: format_siege(get_value(raw_ul, "siege")),
        "DIRIGEANTS": lambda: format_dirigeants(
            get_value(raw_ul, "dirigeants_pp"),
            get_value(raw_ul, "dirigeants_pm"),
        ),
        "FINANCES": lambda: format_bilan(get_value(raw_ul, "bilan_financier")),
        "COMPLEMENTS": lambda: format_complements(raw_ul),
        "MATCHING_ETABLISSEMENTS": lambda: format_etablissements_list(
            get_value(search_result, "matching_etablissements")
        ),
        "SLUG": lambda: get_value(raw_ul, "slug"),
        "ETABLISSEMENTS": lambda: format_etablissements_list(
            get_value(raw_ul, "etablissements")
        ),
        "IMMATRICULATION": lambda: format_immatriculation(
            get_value(raw_ul, "immatriculation")
        ),
        "BODACC": lambda: format_bodacc(get_value(raw_ul, "bodacc")),
        "SCORE": lambda: search_result.get("meta", {}).get("score"),
    }

    for field in fields_to_include:
        handler = handlers.get(field)
        if handler:
            setattr(ul, field.lower(), handler())

    return ul


# -------------------------
# Visibility / ND rules
# -------------------------


def apply_visibility_rules(formatted_ul, raw_ul):
    is_nd = is_unite_legale_non_diffusible(raw_ul)
    is_pm = raw_ul.get("est_personne_morale_insee")

    result_dict = formatted_ul.dict(exclude_unset=True)

    if is_nd:
        return mask_unite_legale(result_dict, is_pm=is_pm, is_ul_nd=is_nd)

    return result_dict


# -------------------------
# Main formatter
# -------------------------


def format_single_unite_legale(search_result, search_params):
    raw_unite_legale = search_result["unite_legale"]

    # 1. Build base object
    formatted_unite_legale = build_unite_legale_base(raw_unite_legale)

    # 2. Enrich based on requested fields
    fields_to_include = create_fields_to_include(
        search_params
    ) + create_admin_fields_to_include(search_params)

    enriched_unite_legale = enrich_unite_legale(
        formatted_unite_legale, search_result, raw_unite_legale, fields_to_include
    )

    # 3. Dev meta
    if is_dev_env():
        enriched_unite_legale.meta = json.loads(
            json.dumps(search_result.get("meta"), default=str)
        )

    # 4. Apply ND masking rules
    return apply_visibility_rules(enriched_unite_legale, raw_unite_legale)



def format_search_results(results, search_params):
    """Main formatting function for all results."""
    formatted_results = []

    for search_result in results:
        # If structure is unite légale
        if "unite_legale" in search_result:
            formatted_results.append(
                format_single_unite_legale(search_result, search_params)
            )

    return formatted_results
