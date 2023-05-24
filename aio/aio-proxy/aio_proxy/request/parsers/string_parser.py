def clean_parameter(request, param: str):
    """Extract and clean param from request.
    Remove white spaces and use upper case.

    Args:
        request: HTTP request
        param (str): parameter to extract from request

    Returns:
        None if None.
        clean_param otherwise.
    """
    param = parse_parameter(request, param)
    if param is None:
        return None
    param_clean = param.replace(" ", "").upper()
    return param_clean


def parse_parameter(request, param: str, default_value=None):
    param = request.rel_url.query.get(param, default_value)
    if param is None:
        return None
    param = param.replace("-", " ").lower()
    return param
