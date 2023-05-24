def ban_params(request, param):
    banned_param = request.rel_url.query.get(param)
    if banned_param:
        raise ValueError(f"Le paramètre {param} n'existe pas.")
