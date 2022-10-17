import re
from typing import Optional


def validate_is_field(request, param: str, default_value=None) -> Optional[str]:
    """Check the validity of field.

    Args:
        param (str): parameter to extract from request

    Returns:
        None if value is not correct.
        is_exist if valid.

    Raises:
        ValueError: if field not valid.
    """
    is_exist = request.rel_url.query.get(param, default_value)
    if is_exist is None:
        return None
    if is_exist not in ["yes"]:
        raise ValueError("{} doit prendre la valeur 'yes' !".format(param))
    return is_exist
