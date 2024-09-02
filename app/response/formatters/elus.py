from app.response.helpers import get_value
from app.response.unite_legale_model import Elu
from app.utils.helpers import convert_to_year_month


def format_elus(elus=None):
    formatted_elus = []
    if elus:
        for elu in elus:
            annee_de_naissance = (
                convert_to_year_month(get_value(elu, "date_naissance"))
                if get_value(elu, "date_naissance")
                else None
            )

            formatted_elu = Elu(
                nom=get_value(elu, "nom"),
                prenoms=get_value(elu, "prenom"),
                annee_de_naissance=annee_de_naissance,
                fonction=get_value(elu, "fonction"),
                sexe=get_value(elu, "sexe"),
            )
            formatted_elus.append(formatted_elu.dict())
    return formatted_elus
