from pydantic import BaseModel


class SearchParams(BaseModel):
    """Class for modeling search parameters"""

    page: int = 1
    per_page: int = 10
    terms: str | None = None
    activite_principale_unite_legale: list | None = None
    categorie_entreprise: list | None = None
    commune: list | None = None
    code_postal: list | None = None
    departement: list | None = None
    region: list | None = None
    est_entrepreneur_individuel: bool | None = None
    section_activite_principale: list | None = None
    tranche_effectif_salarie_unite_legale: list | None = None
    convention_collective_renseignee: bool | None = None
    egapro_renseignee: bool | None = None
    est_bio: bool | None = None
    est_finess: bool | None = None
    est_uai: bool | None = None
    est_collectivite_territoriale: bool | None = None
    est_entrepreneur_spectacle: bool | None = None
    est_association: bool | None = None
    est_organisme_formation: bool | None = None
    est_qualiopi: bool | None = None
    est_rge: bool | None = None
    est_service_public: bool | None = None
    est_societe_mission: bool | None = None
    economie_sociale_solidaire_unite_legale: str | None = None
    id_convention_collective: str | None = None
    id_finess: str | None = None
    id_uai: str | None = None
    code_collectivite_territoriale: str | None = None
    id_rge: str | None = None
    nom_personne: str | None = None
    prenoms_personne: str | None = None
    min_date_naiss_personne: str | None = None
    max_date_naiss_personne: str | None = None
    ca_min: str | None = None
    ca_max: str | None = None
    resultat_net_min: float | None = None
    resultat_net_max: float | None = None
    type_personne: str | None = None
    etat_administratif_unite_legale: str | None = None
    nature_juridique_unite_legale: list | None = None
    matching_size: int | None = 10
    lat: float | None = None
    lon: float | None = None
    radius: float | None = None
    minimal: bool | None = False
    include: list | None = None
    include_admin: list | None = None

