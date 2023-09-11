def parse_and_validate_int(request, param: str, default_value=None):
    int_val = request.rel_url.query.get(param, default_value)
    if int_val is None:
        return None
    try:
        int_val = int(int_val)
    except ValueError:
        raise ValueError("Veuillez indiquer un entier. Exemple : 100000")

    # Elasticsearch `long` type maxes out at this range
    min_val = -9223372036854775295
    max_val = 9223372036854775295

    if min_val <= int_val <= max_val:
        return int_val
    else:
        raise ValueError(f"Veuillez indiquer un entier entre {min_val} et {max_val}.")
