from app.service.formatters.non_diffusible import (
    _ETABLISSEMENT_LIST_FIELDS,
    _ETABLISSEMENT_MASK_FIELDS,
)

PROTEGE_MASK = "[PROTÉGÉ]"

_UL_DENOMINATION_FIELDS = ("nom_complet", "nom_raison_sociale", "sigle")

_DIRIGEANT_PP_PROTEGE_MASK_FIELDS = {
    "nom",
    "prenoms",
    "nationalite",
    "date_de_naissance",
    "annee_de_naissance",
}

# -------------------------
# Dirigeants
# -------------------------


def mask_dirigeant_pp_protege(dirigeant):
    """Mask personal data of a protected PP dirigeant even if field is empty."""
    for field in _DIRIGEANT_PP_PROTEGE_MASK_FIELDS:
        setattr(dirigeant, field, PROTEGE_MASK)
    return dirigeant


# -------------------------
# Etablissement
# -------------------------


def _mask_etablissement_protege_legacy(etab):
    """Mask address fields, even empty values."""
    for field in _ETABLISSEMENT_MASK_FIELDS:
        etab[field] = PROTEGE_MASK
    return etab


def _mask_denomination_etablissement_protege_legacy(etab):
    """Mask even empty fields, so the response does not reveal which ones exist."""
    etab["liste_enseignes"] = [PROTEGE_MASK]
    etab["nom_commercial"] = PROTEGE_MASK
    return etab


def mask_denomination_protege_legacy(formatted_ul):
    """Mask the denomination of a protected legacy unité légale that is not a PM,
    even empty fields, so the response does not reveal which ones exist."""
    for field in _UL_DENOMINATION_FIELDS:
        formatted_ul[field] = PROTEGE_MASK
    if formatted_ul.get("siege"):
        _mask_denomination_etablissement_protege_legacy(formatted_ul["siege"])
    for key in _ETABLISSEMENT_LIST_FIELDS:
        for etab in formatted_ul.get(key) or []:
            _mask_denomination_etablissement_protege_legacy(etab)
    return formatted_ul


def mask_adresses_protege_legacy(formatted_ul):
    """Mask the address of the siege and of every etablissement in-place."""
    if formatted_ul.get("siege"):
        _mask_etablissement_protege_legacy(formatted_ul["siege"])
    for key in _ETABLISSEMENT_LIST_FIELDS:
        for etab in formatted_ul.get(key) or []:
            _mask_etablissement_protege_legacy(etab)
    return formatted_ul
