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
    hide_non_diffusible_fields,
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

ETABLISSEMENT_LIST_FIELDS = ("matching_etablissements", "etablissements")


def get_field(data, field, default=None):
    value = data.get(field, default)
    return default if value is None else value


def is_unite_legale_non_diffusible(data):
    return data.get("statut_diffusion_unite_legale") == "P"


# -------------------------
# Base builder
# -------------------------


def build_unite_legale_base(data):
    is_nd = is_unite_legale_non_diffusible(data)

    fields = {
        "siren": get_field(data, "siren"),
        "nom_complet": format_nom_complet(
            get_field(data, "nom_complet"),
            get_field(data, "sigle"),
            get_nom_commercial(get_field(data, "siege")),
            get_field(data, "est_personne_morale_insee"),
            is_nd,
        ),
        "nom_raison_sociale": get_field(data, "nom_raison_sociale"),
        "sigle": get_field(data, "sigle"),
        "nombre_etablissements": int(get_field(data, "nombre_etablissements", 0)),
        "nombre_etablissements_ouverts": int(
            get_field(data, "nombre_etablissements_ouverts", 0)
        ),
        "activite_principale": get_field(data, "activite_principale_unite_legale"),
        "activite_principale_naf25": get_field(
            data, "activite_principale_naf25_unite_legale"
        ),
        "categorie_entreprise": get_field(data, "categorie_entreprise"),
        "caractere_employeur": get_field(data, "caractere_employeur"),
        "annee_categorie_entreprise": get_field(data, "annee_categorie_entreprise"),
        "date_creation": get_field(data, "date_creation_unite_legale"),
        "date_fermeture": get_field(data, "date_fermeture"),
        "date_mise_a_jour": get_field(data, "date_mise_a_jour"),
        "date_mise_a_jour_insee": get_field(data, "date_mise_a_jour_insee"),
        "date_mise_a_jour_rne": get_field(data, "date_mise_a_jour_rne"),
        "etat_administratif": get_field(data, "etat_administratif_unite_legale"),
        "nature_juridique": format_nature_juridique(
            get_field(data, "nature_juridique_unite_legale")
        ),
        "section_activite_principale": get_field(data, "section_activite_principale"),
        "tranche_effectif_salarie": get_field(
            data, "tranche_effectif_salarie_unite_legale"
        ),
        "annee_tranche_effectif_salarie": get_field(
            data, "annee_tranche_effectif_salarie"
        ),
        "statut_diffusion": get_field(data, "statut_diffusion_unite_legale"),
    }

    return UniteLegaleResponse(**fields)


# -------------------------
# Field enrichment (dispatch map)
# -------------------------


def enrich_unite_legale(obj, result, data, fields_to_include):
    handlers = {
        "SIEGE": lambda: format_siege(get_field(data, "siege")),
        "DIRIGEANTS": lambda: format_dirigeants(
            get_field(data, "dirigeants_pp"),
            get_field(data, "dirigeants_pm"),
        ),
        "FINANCES": lambda: format_bilan(get_field(data, "bilan_financier")),
        "COMPLEMENTS": lambda: format_complements(data),
        "MATCHING_ETABLISSEMENTS": lambda: format_etablissements_list(
            get_value(result, "matching_etablissements")
        ),
        "SLUG": lambda: get_field(data, "slug"),
        "ETABLISSEMENTS": lambda: format_etablissements_list(
            get_field(data, "etablissements")
        ),
        "IMMATRICULATION": lambda: format_immatriculation(
            get_field(data, "immatriculation")
        ),
        "BODACC": lambda: format_bodacc(get_field(data, "bodacc")),
        "SCORE": lambda: result.get("meta", {}).get("score"),
    }

    for field in fields_to_include:
        handler = handlers.get(field)
        if handler:
            setattr(obj, field.lower(), handler())

    return obj


# -------------------------
# Visibility / ND rules
# -------------------------


def apply_visibility_rules(obj, data):
    is_nd = is_unite_legale_non_diffusible(data)
    is_pm = data.get("est_personne_morale_insee")

    result_dict = obj.dict(exclude_unset=True)

    if is_nd:
        return hide_non_diffusible_fields(result_dict, is_pm)

    return result_dict


# -------------------------
# Main formatter
# -------------------------


def format_single_unite_legale(result, search_params):
    data = result["unite_legale"]

    # 1. Build base object
    obj = build_unite_legale_base(data)

    # 2. Enrich based on requested fields
    fields_to_include = create_fields_to_include(
        search_params
    ) + create_admin_fields_to_include(search_params)

    obj = enrich_unite_legale(obj, result, data, fields_to_include)

    # 3. Dev meta
    if is_dev_env():
        obj.meta = json.loads(json.dumps(result.get("meta"), default=str))

    # 4. Apply ND masking rules
    return apply_visibility_rules(obj, data)


def format_search_results(results, search_params):
    """Main formatting function for all results."""
    formatted_results = []

    for result in results:
        # If structure is unite légale
        if "unite_legale" in result:
            formatted_results.append(format_single_unite_legale(result, search_params))

    return formatted_results
