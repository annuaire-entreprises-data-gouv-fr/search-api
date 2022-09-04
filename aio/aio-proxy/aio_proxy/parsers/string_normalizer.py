from unicodedata import normalize


def parse_and_normalize_parameter(request, param: str, default_value=None):
    param = request.rel_url.query.get(param, default_value)
    if param is None:
        return None
    norm_param = (
        normalize("NFD", param.lower().strip())
        .encode("ascii", errors="ignore")
        .decode()
    )
    return norm_param
