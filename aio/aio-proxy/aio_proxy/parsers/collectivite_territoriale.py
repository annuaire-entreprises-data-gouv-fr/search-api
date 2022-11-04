from typing import Optional


def validate_code_collectivite_territoriale(
    code_collectivite_territoriale: str,
) -> Optional[str]:
    """Check the validity of code_collectivite_territoriale

    Args:
        code_collectivite_territoriale(str, optional): id Code Collectivité Territoriale

    Returns:
        None if code_collectivite_territoriale is None.
        code_collectivite_territoriale if valid.

    Raises:
        ValueError: if code_collectivite_territoriale not valid.
    """
    if code_collectivite_territoriale is None:
        return None
    if len(code_collectivite_territoriale) < 2:
        raise ValueError(
            "L'identifiant code_insee d'une collectivité territoriale doit contenir"
            " au moins 2 caractères."
        )
    return code_collectivite_territoriale
