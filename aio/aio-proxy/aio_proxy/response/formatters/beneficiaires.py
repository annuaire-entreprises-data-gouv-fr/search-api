from aio_proxy.response.helpers import get_value
from aio_proxy.response.unite_legale_model import (
    Beneficiaires,
)


def format_beneficiaires(beneficiaires=None):
    beneficiaires_formatted = []
    if beneficiaires:
        for beneficiaire in beneficiaires:
            nom = get_value(beneficiaire, "nom")
            prenoms = get_value(beneficiaire, "prenoms")
            date_de_naissance = get_value(beneficiaire, "date_de_naissance")
            nationalite = get_value(beneficiaire, "nationalite")

            # Only append if at least one field is not None
            if any(
                field is not None
                for field in [nom, prenoms, date_de_naissance, nationalite]
            ):
                beneficiaire_formatted = Beneficiaires(
                    nom=nom,
                    prenoms=prenoms,
                    date_de_naissance=date_de_naissance,
                    nationalite=nationalite,
                )
                beneficiaires_formatted.append(beneficiaire_formatted)
    return beneficiaires_formatted if beneficiaires_formatted else None
