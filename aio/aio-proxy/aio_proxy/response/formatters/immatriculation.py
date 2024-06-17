import json

from aio_proxy.labels.helpers import NATURES_ENTREPRISES
from aio_proxy.response.helpers import convert_date_to_iso
from aio_proxy.response.unite_legale_model import Immatriculation


def format_immatriculation(immatriculation):
    def get_field(field, default=None):
        return immatriculation.get(field, default)

    if not immatriculation:
        return None

    else:
        return Immatriculation(
            date_debut_activite=convert_date_to_iso(get_field("date_debut_activite")),
            date_immatriculation=convert_date_to_iso(get_field("date_immatriculation")),
            date_radiation=convert_date_to_iso(get_field("date_radiation")),
            duree_personne_morale=get_field("duree_personne_morale"),
            nature_entreprise=format_nature_entreprise(get_field("nature_entreprise")),
            date_cloture_exercice=(get_field("date_cloture_exercice")),
            capital_social=get_field("capital_social"),
            capital_variable=get_field("capital_variable"),
            devise_capital=get_field("devise_capital"),
            indicateur_associe_unique=get_field("indicateur_associe_unique"),
        ).dict()


def format_nature_entreprise(nature_entreprise):
    # Load nature_entreprise from JSON string
    nature_entreprise_list = json.loads(nature_entreprise)

    if nature_entreprise_list is None:
        return None

    mapped_nature_entreprise = []

    for code in nature_entreprise_list:
        if code in NATURES_ENTREPRISES:
            mapped_nature_entreprise.append(NATURES_ENTREPRISES[code])
        else:
            mapped_nature_entreprise.append(code)  # return nature as is if not found

    return mapped_nature_entreprise
