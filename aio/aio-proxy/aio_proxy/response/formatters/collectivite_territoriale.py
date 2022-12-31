from aio_proxy.response.formatters.elus import format_elus


def format_collectivite_territoriale(
    colter_code=None, colter_code_insee=None, colter_elus=None, colter_niveau=None
):
    if colter_code is None:
        return None
    else:
        return {
            "code": colter_code,
            "code_insee": colter_code_insee,
            "elus": format_elus(colter_elus),
            "niveau": colter_niveau,
        }
