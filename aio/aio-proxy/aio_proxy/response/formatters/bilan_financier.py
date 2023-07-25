from aio_proxy.response.helpers import get_value


def format_bilan(source_bilan):
    if source_bilan:
        formatted_bilan = {
            get_value(source_bilan, "annee_cloture_exercice"): {
                "ca": get_value(source_bilan, "ca"),
                "resultat_net": get_value(source_bilan, "resultat_net"),
            }
        }
        return formatted_bilan
    return {}
