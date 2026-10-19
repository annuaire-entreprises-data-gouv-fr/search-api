from app.models.unite_legale import Opco


def format_opco(opco: str | None, opco_gestion: str | None) -> Opco | None:
    if not opco:
        return None
    return Opco(nom=opco, nom_gestion=opco_gestion)
