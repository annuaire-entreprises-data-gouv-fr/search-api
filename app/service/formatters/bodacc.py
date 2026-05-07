from app.models.unite_legale import Bodacc, BodaccProcedureCollective, BodaccRadiation


def format_bodacc(bodacc):
    radiation_fields = bodacc.get("radiation")
    procedure_fields = bodacc.get("procedure_collective")

    return Bodacc(
        radiation=BodaccRadiation(**radiation_fields) if radiation_fields else None,
        procedure_collective=BodaccProcedureCollective(**procedure_fields)
        if procedure_fields
        else None,
    )
