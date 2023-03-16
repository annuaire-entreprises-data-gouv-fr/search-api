from aio_proxy.response.helpers import get_value


def format_bilan(source_bilan):
    if source_bilan:
        formatted_bilan = {
            "ca": get_value(source_bilan, "ca"),
            "resultat_net": get_value(source_bilan, "resultat_net"),
            "date_cloture_exercice": get_value(source_bilan, "date_cloture_exercice"),
        }
        return formatted_bilan
    return {}
