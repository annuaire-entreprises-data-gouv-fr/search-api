from app.response.helpers import get_value
from app.response.unite_legale_model import (
    DirigeantsPM,
    DirigeantsPP,
)


def format_dirigeants(dirigeants_pp=None, dirigeants_pm=None):
    dirigeants = []
    if dirigeants_pp:
        for dirigeant_pp in dirigeants_pp:
            annee_de_naissance = (
                get_value(dirigeant_pp, "date_de_naissance")[:4]
                if get_value(dirigeant_pp, "date_de_naissance")
                else None
            )
            dirigeant = DirigeantsPP(
                nom=get_value(dirigeant_pp, "nom"),
                prenoms=get_value(dirigeant_pp, "prenoms"),
                annee_de_naissance=annee_de_naissance,
                date_de_naissance=get_value(dirigeant_pp, "date_de_naissance"),
                qualite=get_value(dirigeant_pp, "role"),
                nationalite=get_value(dirigeant_pp, "nationalite"),
                type_dirigeant="personne physique",
            )
            dirigeants.append(dirigeant)
    if dirigeants_pm:
        for dirigeant_pm in dirigeants_pm:
            dirigeant = DirigeantsPM(
                siren=get_value(dirigeant_pm, "siren"),
                denomination=get_value(dirigeant_pm, "denomination"),
                qualite=get_value(dirigeant_pm, "role"),
                type_dirigeant="personne morale",
            )
            dirigeants.append(dirigeant)
    return dirigeants
