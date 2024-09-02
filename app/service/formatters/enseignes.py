def format_enseignes(enseignes):
    enseignes_filtered = [enseigne for enseigne in enseignes if enseigne is not None]
    if not enseignes_filtered:
        return None
    return enseignes_filtered
