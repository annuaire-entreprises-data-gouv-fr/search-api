def parse_and_validate_per_page(request) -> int:
    try:
        per_page = int(request.rel_url.query.get("per_page", 10))  # default 10
    except (TypeError, ValueError):
        raise ValueError("Veuillez indiquer un `per_page` entier, par défaut 10.")
    return per_page
