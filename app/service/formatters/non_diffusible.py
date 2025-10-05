NON_DIFFUSIBLE_MASK = "[NON-DIFFUSIBLE]"

# Unite légale fields to hide for ND depending on person type
_UL_PM_FIELDS_TO_MASK = ["sigle"]

_UL_PP_FIELDS_TO_MASK = [
    "nom_complet",
    "nom_raison_sociale",
    "sigle",
]

# fields that must be masked for établissements
_ETABLISSEMENT_FIELDS_TO_MASK = [
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
    "type_voie",
]

# Dirigeant fields to hide for personne physique
_DIRIGEANT_PP_FIELDS_TO_MASK = [
    "nom",
    "prenoms",
    "annee_de_naissance",
    "date_de_naissance",
]


def _mask_fields(mapping, fields):
    """Mask specified fields in mapping with NON_DIFFUSIBLE_MASK if present."""
    for field in fields:
        if field in mapping:
            mapping[field] = NON_DIFFUSIBLE_MASK


def hide_non_diffusible_unite_legale(result_formatted, est_personne_morale_insee):
    """
    Hide non-diffusible fields based on entity type.

    For personne morale in Insee, only hide 'sigle'.
    For personne physique or non doté de personne morale, hide 'nom_complet',
    'nom_raison_sociale', and 'sigle'.
    """
    # Mask unite legale fields
    hidden_fields = (
        _UL_PM_FIELDS_TO_MASK if est_personne_morale_insee else _UL_PP_FIELDS_TO_MASK
    )
    _mask_fields(result_formatted, hidden_fields)

    # Handle siege (show denomination for PM, hide for PP)
    if result_formatted.get("siege"):
        hide_non_diffusible_etablissement_fields(
            result_formatted["siege"], hide_denomination=not est_personne_morale_insee
        )

    # Handle dirigeants
    if result_formatted.get("dirigeants"):
        hide_non_diffusible_dirigeants_fields(result_formatted["dirigeants"])

    # Handle all other établissements (always hide denomination)
    for etab_list_key in ("matching_etablissements", "etablissements"):
        for etablissement in result_formatted.get(etab_list_key, []):
            hide_non_diffusible_etablissement_fields(
                etablissement, hide_denomination=True
            )

    return result_formatted


# Backward-compatible entry point used elsewhere in the codebase
def hide_non_diffusible_fields(result_formatted, est_personne_morale_insee):
    """Legacy function name maintained for backward compatibility."""
    return hide_non_diffusible_unite_legale(result_formatted, est_personne_morale_insee)


def hide_non_diffusible_dirigeants_fields(dirigeants):
    """Mask personne physique fields for all dirigeants of type 'personne physique'."""
    for dirigeant in dirigeants:
        if dirigeant.get("type_dirigeant") == "personne physique":
            _mask_fields(dirigeant, _DIRIGEANT_PP_FIELDS_TO_MASK)
    return dirigeants



def hide_non_diffusible_etablissement_fields(etablissement, hide_denomination):
    """
    Mask non-diffusible établissement fields.

    Args:
        etablissement: The établissement dict to modify in-place
        hide_denomination: If True, also mask nom_commercial and liste_enseignes
    """
    # Mask denomination fields if requested
    if hide_denomination:
        liste_enseignes = etablissement.get("liste_enseignes")
        if liste_enseignes:
            etablissement["liste_enseignes"] = [NON_DIFFUSIBLE_MASK] * len(
                liste_enseignes
            )

        _mask_fields(etablissement, ["nom_commercial"])

    # Mask address fields
    _mask_fields(etablissement, _ETABLISSEMENT_FIELDS_TO_MASK)
    return etablissement
