from app.models.unite_legale import Bodacc
from app.utils.helpers import convert_date_to_iso


def format_bodacc(bodacc):
    if not bodacc:
        bodacc = {}

    def get_field(field, default=None):
        return bodacc.get(field, default)

    return Bodacc(
        est_radie_rcs=get_field("est_radie_rcs"),
        radiation_rcs_date=convert_date_to_iso(get_field("radiation_rcs_date")),
        procedure_collective_date=convert_date_to_iso(
            get_field("procedure_collective_date")
        ),
        procedure_collective_nature=get_field("procedure_collective_nature"),
    )
