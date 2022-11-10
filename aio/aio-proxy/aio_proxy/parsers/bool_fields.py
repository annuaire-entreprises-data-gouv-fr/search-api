from typing import Optional


def validate_bool_field(param: str, param_value: str) -> Optional[bool]:
    """Check the validity of field.

    Args:
        param (str): param extracted from request
        param_value (str): param_value extracted from request

    Returns:
        None if value is not correct.
        param_value if valid.

    Raises:
        ValueError: if field not valid.
    """
    if param_value is None:
        return None
    if param_value not in ["TRUE", "FALSE"]:
        raise ValueError(f"{param} doit prendre la valeur 'true' or 'false' !")
    return param_value == "TRUE"
