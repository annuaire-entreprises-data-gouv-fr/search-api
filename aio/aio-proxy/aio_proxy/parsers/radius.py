def parse_and_validate_radius(request):
    try:
        radius = float(request.rel_url.query.get("radius", 5))  # default 5
        return radius
    except (TypeError, ValueError):
        raise ValueError("Veuillez indiquer un radius entier ou flottant, en km.")
