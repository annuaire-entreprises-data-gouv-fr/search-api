from app.labels.helpers import NATURES_JURIDIQUES


def format_nature_juridique(nature_juridique):
    if nature_juridique not in NATURES_JURIDIQUES:
        return None
    else:
        return nature_juridique
