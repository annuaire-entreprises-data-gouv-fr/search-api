def get_nom_commercial(siege):
    return siege.get("nom_commercial", None) if siege else None


def format_nom_complet(
    nom_complet,
    sigle=None,
    nom_commercial_siege=None,
    denomination_usuelle_1=None,
    denomination_usuelle_2=None,
    denomination_usuelle_3=None,
):
    """Add `denomination usuelle` fields and `sigle` to `nom_complet`."""
    if not nom_complet:
        return None

    # Handle denomination usuelle
    if nom_commercial_siege:
        denomination = nom_commercial_siege
    else:
        denomination = " ".join(
            filter(
                lambda x: x and x.upper() != "SUPPRESSION DU NOM COMMERCIAL",
                [
                    denomination_usuelle_1,
                    denomination_usuelle_2,
                    denomination_usuelle_3,
                ],
            )
        )

    # Add denomination to nom_complet if it exists
    if denomination:
        nom_complet += f" ({denomination.strip()})"

    # Add sigle if it exists
    if sigle:
        nom_complet += f" ({sigle})"

    return nom_complet.upper()
