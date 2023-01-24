from typing import List


def validate_code_collectivite_territoriale(
    list_code_collectivite_territoriale: List[str],
):
    """Check the validity of list code_collectivite_territoriale

    Args:
        list_code_collectivite_territoriale(list(str), optional): ids Codes
        Collectivité Territoriale

    Returns:
        None if list_code_collectivite_territoriale is None.
        list_code_collectivite_territoriale if valid.

    Raises:
        ValueError: if one of the values in list_code_collectivite_territoriale is
        not valid.
    """
    if list_code_collectivite_territoriale is None:
        return None
    for code_collectivite_territoriale in list_code_collectivite_territoriale:
        if len(code_collectivite_territoriale) < 2:
            raise ValueError(
                "Chaque identifiant code insee d'une collectivité territoriale doit "
                "contenir au moins 2 caractères."
            )
    return list_code_collectivite_territoriale
