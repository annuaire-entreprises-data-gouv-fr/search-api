from pydantic import BaseModel


class FondationResponse(BaseModel):
    numero_rnf: str | None = None
    titre: str | None = None
    type_organisme: str | None = None
    date_creation: str | None = None
    adresse: str | None = None
    code_postal: str | None = None
    ville: str | None = None
    siren: str | None = None
    siret: str | None = None
    score: float | None = None
    meta: dict | None = None
