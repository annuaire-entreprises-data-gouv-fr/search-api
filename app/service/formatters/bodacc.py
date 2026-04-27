from app.models.unite_legale import Bodacc
from app.utils.helpers import convert_date_to_iso


def format_bodacc(bodacc):
    if not bodacc:
        bodacc = {}

    def get_field(field, default=None):
        return bodacc.get(field, default)

    return Bodacc(
        radiation_rcs=get_field("radiation_rcs") or False,
        radiation_rcs_date=convert_date_to_iso(get_field("radiation_rcs_date")),
        procedure_collective_date_jugement=convert_date_to_iso(
            get_field("procedure_collective_date_jugement")
        ),
        procedure_collective_nature=get_field("procedure_collective_nature"),
    )
