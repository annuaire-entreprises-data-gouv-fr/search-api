def filter_by_siren(search, siren_string):
    """Filter by `siren` number"""
    search = search.filter("term", **{"siren": siren_string})
    return search
