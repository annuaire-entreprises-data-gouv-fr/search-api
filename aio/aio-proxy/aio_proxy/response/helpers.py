import json


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return json.dumps(message)


def get_value(dict, key, default=None):
    """Set value to value of key if key found in dict, otherwise set value to
    default."""
    value = dict[key] if key in dict else default
    return value


def format_collectivite_territoriale(
    colter_code=None,
    colter_code_insee=None,
    colter_elus=None,
    colter_niveau=None
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


def format_dirigeants(dirigeants_pp=None, dirigeants_pm=None):
    dirigeants = []
    if dirigeants_pp:
        for dirigeant_pp in dirigeants_pp:
            annee_de_naissance = (
                get_value(dirigeant_pp, "date_naissance")[:4]
                if get_value(dirigeant_pp, "date_naissance")
                else None
            )

            dirigeant = {
                "nom": get_value(dirigeant_pp, "nom"),
                "prenoms": get_value(dirigeant_pp, "prenoms"),
                "annee_de_naissance": annee_de_naissance,
                "qualite": get_value(dirigeant_pp, "qualite"),
            }
            dirigeants.append(dirigeant)
    if dirigeants_pm:
        for dirigeant_pm in dirigeants_pm:
            sigle = (
                get_value(dirigeant_pm, "sigle")
                if get_value(dirigeant_pm, "sigle") != ""
                else None
            )
            dirigeant = {
                "siren": get_value(dirigeant_pm, "siren"),
                "denomination": get_value(dirigeant_pm, "denomination"),
                "sigle": sigle,
                "qualite": get_value(dirigeant_pm, "qualite"),
            }
            dirigeants.append(dirigeant)
    return dirigeants


def format_elus(elus=None):
    format_elus = []
    if elus:
        for elu in elus:
            annee_de_naissance = (
                get_value(elu, "date_naissance")[:4]
                if get_value(elu, "date_naissance")
                else None
            )

            format_elu = {
                "nom": get_value(elu, "nom"),
                "prenoms": get_value(elu, "prenom"),
                "annee_de_naissance": annee_de_naissance,
                "fonction": get_value(elu, "fonction"),
                "sexe": get_value(elu, "sexe"),
            }
            format_elus.append(format_elu)
    return format_elus


def format_est_field(value):
    if value is None:
        return False
    else:
        return True
