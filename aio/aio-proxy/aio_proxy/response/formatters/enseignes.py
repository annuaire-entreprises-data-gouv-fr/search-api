def format_enseignes(enseignes):
    if not enseignes:
        return None
    return [enseigne for enseigne in enseignes if enseigne is not None]
