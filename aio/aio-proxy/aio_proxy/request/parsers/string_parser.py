def clean_parameter(param: str):
    """Extract and clean param from request.
    Remove white spaces and use upper case.

    Args:
        request: HTTP request
        param (str): parameter to extract from request

    Returns:
        None if None.
        clean_param otherwise.
    """
    if param is None:
        return None
    param = param.replace("-", " ")
    param_clean = param.replace(" ", "").upper()
    return param_clean
