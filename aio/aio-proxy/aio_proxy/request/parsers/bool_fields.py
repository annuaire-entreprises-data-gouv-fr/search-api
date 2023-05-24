from aio_proxy.request.parsers.string_parser import clean_parameter


def parse_and_validate_bool_field(request, param: str) -> bool | None:
    """Check the validity of field.

    Args:
        request: http request
        param (str): param extracted from request

    Returns:
        None if value is not correct.
        param_value if valid.

    Raises:
        ValueError: if field not valid.
    """
    param_value = clean_parameter(request, param)
    if param_value is None:
        return None
    if param_value not in ["TRUE", "FALSE"]:
        raise ValueError(f"{param} doit prendre la valeur 'true' ou 'false' !")
    return param_value == "TRUE"
