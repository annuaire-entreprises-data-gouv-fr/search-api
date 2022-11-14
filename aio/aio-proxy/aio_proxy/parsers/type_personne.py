from typing import Optional


def validate_type_personne(type_personne_clean: str) -> Optional[str]:
    """Check the validity of type_personne.

    Args:
        type_personne_clean(str, optional): type personne extracted and cleaned.

    Returns:
        None if type_personne_clean is None.
        type_personne_clean if valid.

    Raises:
        ValueError: if type_personne_clean not valid.
    """
    if type_personne_clean is None:
        return None
    if type_personne_clean not in ["ELU, DIRIGEANT"]:
        raise ValueError(f"type_personne doit prendre la valeur 'dirigeant' ou 'elu' !")
    return type_personne_clean
