def parse_and_validate_longitude(request):
    try:
        lon = float(request.rel_url.query.get("long"))
        if lon > 180 or lon < -180:
            raise ValueError
        return lon
    except (TypeError, KeyError, ValueError):
        raise ValueError("Veuillez indiquer une longitude entre -180° et 180°.")
