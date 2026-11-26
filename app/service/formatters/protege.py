from app.service.formatters.non_diffusible import (
    _ETABLISSEMENT_LIST_FIELDS,
    _ETABLISSEMENT_MASK_FIELDS,
)

PROTEGE_MASK = "[PROTÉGÉ]"

# -------------------------
# Dirigeants
# -------------------------

_DIRIGEANT_PP_PROTEGE_MASK_FIELDS = {
    "nom",
    "prenoms",
    "nationalite",
    "date_de_naissance",
    "annee_de_naissance",
}


def mask_dirigeant_pp_protege(dirigeant):
    """Mask personal data of a protected PP dirigeant even if field is empty."""
    for field in _DIRIGEANT_PP_PROTEGE_MASK_FIELDS:
        setattr(dirigeant, field, PROTEGE_MASK)
    return dirigeant


# -------------------------
# Etablissement
# -------------------------

_ETABLISSEMENT_COMMUNE_MASK_FIELDS = (
    "commune",
    "libelle_commune",
    "libelle_commune_etranger",
    "epci",
)


def _mask_etablissement_protege_legacy(etab):
    """Mask address fields, even empty values."""
    for field in _ETABLISSEMENT_MASK_FIELDS:
        etab[field] = PROTEGE_MASK
    return etab


def _mask_commune_etablissement_protege_legacy(etab):
    """Mask commune fields, even empty values."""
    for field in _ETABLISSEMENT_COMMUNE_MASK_FIELDS:
        etab[field] = PROTEGE_MASK
    return etab


def _mask_denomination_etablissement_protege_legacy(etab):
    """Mask the enseignes and nom commercial of every établissement with the protégé label."""
    etab["liste_enseignes"] = [PROTEGE_MASK]
    etab["nom_commercial"] = PROTEGE_MASK
    return etab


def mask_adresses_protege_legacy(formatted_ul):
    """Mask the address of the siege and of every établissement with the protégé label."""
    if formatted_ul.get("siege"):
        _mask_etablissement_protege_legacy(formatted_ul["siege"])
    for key in _ETABLISSEMENT_LIST_FIELDS:
        for etab in formatted_ul.get(key) or []:
            _mask_etablissement_protege_legacy(etab)
    return formatted_ul


def mask_communes_protege_legacy(formatted_ul):
    """Mask the commune of every établissement with the protégé label."""
    if formatted_ul.get("siege"):
        _mask_commune_etablissement_protege_legacy(formatted_ul["siege"])
    for key in _ETABLISSEMENT_LIST_FIELDS:
        for etab in formatted_ul.get(key) or []:
            _mask_commune_etablissement_protege_legacy(etab)
    return formatted_ul


# -------------------------
# Unité Légale
# -------------------------

_UL_DENOMINATION_FIELDS = ("nom_complet", "nom_raison_sociale", "sigle")


def mask_noms_de_domaine_protege(formatted_ul):
    """Mask the domain names with a single protégé label."""
    formatted_ul["noms_de_domaine"] = [PROTEGE_MASK]
    return formatted_ul


def mask_denomination_protege_legacy(formatted_ul):
    """Mask the démomination of the unité légale with the protégé label."""
    for field in _UL_DENOMINATION_FIELDS:
        formatted_ul[field] = PROTEGE_MASK
    mask_noms_de_domaine_protege(formatted_ul)
    if formatted_ul.get("siege"):
        _mask_denomination_etablissement_protege_legacy(formatted_ul["siege"])
    for key in _ETABLISSEMENT_LIST_FIELDS:
        for etab in formatted_ul.get(key) or []:
            _mask_denomination_etablissement_protege_legacy(etab)
    return formatted_ul
