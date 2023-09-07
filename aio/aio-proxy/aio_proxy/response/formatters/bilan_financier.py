from aio_proxy.response.unite_legale_model import Finances


def format_bilan(source_bilan):
    if source_bilan:
        formatted_bilan = {
            source_bilan.get("annee_cloture_exercice"): Finances(
                ca=source_bilan.get("ca"),
                resultat_net=source_bilan.get("resultat_net"),
            )
        }
        return formatted_bilan
    return {}
