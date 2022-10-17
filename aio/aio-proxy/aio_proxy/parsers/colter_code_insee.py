from typing import Optional

def validate_colter_code_insee(colter_code_insee: str) -> Optional[str]:
    """Check the validity of colter_code_insee.

    Args:
        colter_code_insee(str, optional): id Code Insee Collectivité Territoriale

    Returns:
        None if colter_code_insee is None.
        colter_code_insee if valid.

    Raises:
        ValueError: if colter_code_insee not valid.
    """
    if colter_code_insee is None:
        return None
    if len(colter_code_insee) < 2:
        raise ValueError("L'identifiant code_insee d'une collectivité territoriale doit contenir au moins 2 caractères.")
    return colter_code_insee
