import json

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
            nature_entreprise=json.loads(get_field("nature_entreprise")),
            date_cloture_exercice=(get_field("date_cloture_exercice")),
            capital_social=get_field("capital_social"),
            capital_variable=get_field("capital_variable"),
            devise_capital=get_field("devise_capital"),
            indicateur_associe_unique=get_field("indicateur_associe_unique"),
        ).dict()
