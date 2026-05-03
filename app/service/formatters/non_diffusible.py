NON_DIFFUSIBLE_MASK = "[NON-DIFFUSIBLE]"

# -------------------------
# Masking rules
# -------------------------

# PM : peronne morale
# PP : personne physique
_UL_MASK_FIELDS_PM = {"sigle"}

_UL_MASK_FIELDS_PP = {
    "nom_complet",
    "nom_raison_sociale",
    "sigle",
}

_ETABLISSEMENT_MASK_FIELDS = {
    "adresse",
    "cedex",
    "code_postal",
    "complement_adresse",
    "coordonnees",
    "distribution_speciale",
    "indice_repetition",
    "longitude",
    "latitude",
    "libelle_cedex",
    "libelle_voie",
    "numero_voie",
    "dernier_numero_voie",
    "type_voie",
}

_DIRIGEANT_PP_MASK_FIELDS = {
    "nom",
    "prenoms",
    "annee_de_naissance",
    "date_de_naissance",
    "nationalite",
}

_ETABLISSEMENT_LIST_FIELDS = ("matching_etablissements", "etablissements")


# -------------------------
# Generic helpers
# -------------------------


def _mask_fields(mapping, fields):
    """Mask given fields in-place."""
    for field in fields:
        if field in mapping:
            mapping[field] = NON_DIFFUSIBLE_MASK
    return mapping


# -------------------------
# Dirigeants
# -------------------------


def _mask_dirigeants(dirigeants):
    """Mask personne physique fields for all PP dirigeants."""
    if not dirigeants:
        return dirigeants

    for d in dirigeants:
        if d.get("type_dirigeant") == "personne physique":
            _mask_fields(d, _DIRIGEANT_PP_MASK_FIELDS)

    return dirigeants


# -------------------------
# Etablissement
# -------------------------


def _mask_etablissement(etab, *, hide_denomination: bool):
    """
    Mask non-diffusible fields of an etablissement.

    Args:
        etablissement: The etablissement dict to modify in-place.
        hide_denomination: When True, also mask nom commercial and enseignes.
    """
    if not etab:
        return etab

    # Mask denomination fields
    if hide_denomination:
        if etab.get("liste_enseignes"):
            etab["liste_enseignes"] = [NON_DIFFUSIBLE_MASK] * len(
                etab["liste_enseignes"]
            )

        _mask_fields(etab, {"nom_commercial"})

    # Mask address / geo fields
    _mask_fields(etab, _ETABLISSEMENT_MASK_FIELDS)

    return etab


# -------------------------
# Unite légale (main entry)
# -------------------------


def mask_unite_legale(formatted_ul, *, is_pm: bool, is_ul_nd: bool):
    """
    Mask non-diffusible fields on a formatted unite légale result.

    - Personne morale  → only 'sigle' is masked at the UL level.
    - Personne physique → 'nom_complet', 'nom_raison_sociale', and 'sigle' are masked.

    Siege, dirigeants, and all etablissements are masked accordingly.
    """

    # -----------------
    # Case 1: UL is ND
    # -----------------
    if is_ul_nd:
        fields_to_mask = _UL_MASK_FIELDS_PM if is_pm else _UL_MASK_FIELDS_PP
        _mask_fields(formatted_ul, fields_to_mask)

        # Siege
        if formatted_ul.get("siege"):
            _mask_etablissement(
                formatted_ul["siege"],
                hide_denomination=not is_pm,
            )

        # Dirigeants
        if formatted_ul.get("dirigeants"):
            _mask_dirigeants(formatted_ul["dirigeants"])

        # Etablissements
        for key in _ETABLISSEMENT_LIST_FIELDS:
            for etab in formatted_ul.get(key, []):
                _mask_etablissement(
                    etab,
                    hide_denomination=not is_pm,
                )

        return formatted_ul
