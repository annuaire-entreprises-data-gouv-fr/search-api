def get_nom_commercial(siege: dict | None) -> str | None:
    return siege.get("nom_commercial") if siege else None


def format_nom_complet(
    nom_complet: str | None,
    sigle: str | None = None,
    nom_commercial_siege: str | None = None,
    is_personne_morale_insee: bool = False,
    is_ul_non_diffusible: bool = False,
    is_siege_non_diffusible: bool = False,
) -> str | None:
    """Add `denomination usuelle` fields (if diffusible) and `sigle` to `nom_complet`.

    Returns None if nom_complet is empty.
    """
    if not nom_complet:
        return None

    parts = [nom_complet]

    if nom_commercial_siege and not is_siege_non_diffusible:
        parts.append(f"({nom_commercial_siege.strip()})")

    if sigle and not (is_personne_morale_insee and is_ul_non_diffusible):
        parts.append(f"({sigle})")

    return " ".join(parts).upper()
