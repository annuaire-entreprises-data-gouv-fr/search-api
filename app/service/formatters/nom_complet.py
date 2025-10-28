def get_nom_commercial(siege):
    return siege.get("nom_commercial") if siege else None


def format_nom_complet(
    nom_complet,
    sigle=None,
    nom_commercial_siege=None,
    is_personne_morale_insee=False,
    is_non_diffusible=False,
):
    """Add `denomination usuelle` fields and `sigle` to `nom_complet`.

    Returns None if nom_complet is empty.
    """
    if not nom_complet:
        return None

    # Build denomination from available sources
    denomination = None
    if nom_commercial_siege:
        denomination = nom_commercial_siege

    # Build final name with parenthetical additions
    result = nom_complet
    if denomination:
        result += f" ({denomination.strip()})"
    if sigle and not (is_personne_morale_insee and is_non_diffusible):
        result += f" ({sigle})"

    return result.upper()
