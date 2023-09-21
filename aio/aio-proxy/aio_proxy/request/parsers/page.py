def parse_int(request, param) -> int:
    integer = int(request.rel_url.query.get(param))
    return integer
