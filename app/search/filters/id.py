def filter_by_id(search, id_string):
    """Filter documents by `id`"""
    search = search.filter("term", **{"_id": id_string})
    return search
