from typing import Optional


def validate_etat_administratif(param_value: str) -> Optional[str]:
    """Check the validity of etat_administratif.

    Args:
        param_value (str): param_value extracted from request

    Returns:
        None if value is not correct.
        param_value if valid.

    Raises:
        ValueError: if field not valid.
    """
    if param_value is None:
        return None
    if param_value not in ["A", "C"]:
        raise ValueError(f"L'état administratif doit prendre la valeur 'A' ou 'C' !")
    return param_value
