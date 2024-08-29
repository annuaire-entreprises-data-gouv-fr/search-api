from app.models.unite_legale import CollectiviteTerritoriale
from app.response.formatters.elus import format_elus


def format_collectivite_territoriale(
    colter_code=None,
    colter_code_insee=None,
    colter_elus=None,
    colter_niveau=None,
):
    if colter_code is None:
        return None
    else:
        return CollectiviteTerritoriale(
            code=colter_code,
            code_insee=colter_code_insee,
            elus=format_elus(colter_elus),  # Format elus if provided
            niveau=colter_niveau,
        ).dict()
