from dataclasses import asdict

from aio_proxy.response.helpers import get_value
from aio_proxy.response.unite_legale_model import (
    UniteLegaleDirigeantsPM,
    UniteLegaleDirigeantsPP,
)


def format_dirigeants(dirigeants_pp=None, dirigeants_pm=None, is_non_diffusible=False):
    dirigeants = []
    if dirigeants_pp:
        for dirigeant_pp in dirigeants_pp:
            if is_non_diffusible:
                dirigeant = UniteLegaleDirigeantsPP(
                    nom="[NON-DIFFUSIBLE]",
                    prenoms="[NON-DIFFUSIBLE]",
                    annee_de_naissance="[NON-DIFFUSIBLE]",
                    qualite=get_value(dirigeant_pp, "qualite"),
                    type_dirigeant="personne physique",
                )
            else:
                annee_de_naissance = (
                    get_value(dirigeant_pp, "date_naissance")[:4]
                    if get_value(dirigeant_pp, "date_naissance")
                    else None
                )

                dirigeant = UniteLegaleDirigeantsPP(
                    nom=get_value(dirigeant_pp, "nom"),
                    prenoms=get_value(dirigeant_pp, "prenoms"),
                    annee_de_naissance=annee_de_naissance,
                    qualite=get_value(dirigeant_pp, "qualite"),
                    type_dirigeant="personne physique",
                )
            dirigeants.append(asdict(dirigeant))
    if dirigeants_pm:
        for dirigeant_pm in dirigeants_pm:
            sigle = (
                get_value(dirigeant_pm, "sigle")
                if get_value(dirigeant_pm, "sigle") != ""
                else None
            )
            dirigeant = UniteLegaleDirigeantsPM(
                siren=get_value(dirigeant_pm, "siren"),
                denomination=get_value(dirigeant_pm, "denomination"),
                sigle=sigle,
                qualite=get_value(dirigeant_pm, "qualite"),
                type_dirigeant="personne morale",
            )
            dirigeants.append(asdict(dirigeant))
    return dirigeants
