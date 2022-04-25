def parse_and_validate_latitude(request):
    try:
        lat = float(request.rel_url.query.get("lat"))
        if lat > 90 or lat < -90:
            raise ValueError
        return lat
    except (TypeError, KeyError, ValueError):
        raise ValueError("Veuillez indiquer une latitude entre -90° et 90°.")
