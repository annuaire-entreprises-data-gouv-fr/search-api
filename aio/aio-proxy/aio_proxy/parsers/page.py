def parse_and_validate_page(request) -> int:
    try:
        page = int(request.rel_url.query.get("page", 1)) - 1  # default 1
    except (TypeError, ValueError):
        raise ValueError("Veuillez indiquer un numéro de page entier, par défaut 1.")
    return page
