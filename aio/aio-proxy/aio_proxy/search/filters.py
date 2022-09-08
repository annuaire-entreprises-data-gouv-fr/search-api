def filter_search(search, filters_to_ignore: list, **kwargs):
    """Use filters to reduce search results."""
    for key, value in kwargs.items():
        if value is not None and key not in filters_to_ignore:
            search = search.filter("term", **{key: value})
    return search
