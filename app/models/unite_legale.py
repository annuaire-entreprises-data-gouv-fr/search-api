from typing import Literal

from pydantic import BaseModel, Field


class Etablissement(BaseModel):
    model_config = {"populate_by_name": True}

    activite_principale: str | None = None
    activite_principale_registre_metier: str | None = None
    ancien_siege: bool | None = None
    annee_tranche_effectif_salarie: str | None = None
    adresse: str | None = None
    caractere_employeur: str | None = None
    cedex: str | None = None
    code_pays_etranger: str | None = None
    code_postal: str | None = None
    commune: str | None = None
    complement_adresse: str | None = None
    coordonnees: str | None = None
    date_creation: str | None = None
    date_debut_activite: str | None = None
    date_fermeture: str | None = None
    date_mise_a_jour: str | None = None
    date_mise_a_jour_insee: str | None = None
    departement: str | None = None
    distribution_speciale: str | None = None
    epci: str | None = None
    est_siege: bool = False
    etat_administratif: str | None = None
    geo_adresse: str | None = None
    geo_id: str | None = None
    indice_repetition: str | None = None
    latitude: str | None = None
    libelle_cedex: str | None = None
    libelle_commune: str | None = None
    libelle_commune_etranger: str | None = None
    libelle_pays_etranger: str | None = None
    libelle_voie: str | None = None
    liste_enseignes: list | None = None
    liste_finess_geographique: list | None = Field(
        None, alias="liste_finess", serialization_alias="liste_finess"
    )
    liste_id_bio: list | None = None
    liste_idcc: list | None = None
    liste_id_organisme_formation: list | None = None
    liste_rge: list | None = None
    liste_uai: list | None = None
    longitude: str | None = None
    nom_commercial: str | None = None
    numero_voie: str | None = None
    region: str | None = None
    siret: str | None = None
    statut_diffusion_etablissement: str | None = None
    tranche_effectif_salarie: str | None = None
    type_voie: str | None = None


class Elu(BaseModel):
    nom: str | None = None
    prenoms: str | None = None
    annee_de_naissance: str | None = None
    fonction: str | None = None
    sexe: str | None = None


class DirigeantsPM(BaseModel):
    siren: str | None = None
    denomination: str | None = None
    qualite: str | None = None
    type_dirigeant: Literal["personne morale"]


class DirigeantsPP(BaseModel):
    nom: str | None = None
    prenoms: str | None = None
    annee_de_naissance: str | None = None
    date_de_naissance: str | None = None
    qualite: str | None = None
    nationalite: str | None = None
    type_dirigeant: Literal["personne physique"]


class Finances(BaseModel):
    annee_cloture_exercice: str | None = None
    ca: int | None = None
    resultat_net: int | None = None


class CollectiviteTerritoriale(BaseModel):
    code: str | None = None
    code_insee: str | None = None
    elus: list[Elu] | None = None
    niveau: str | None = None


class Immatriculation(BaseModel):
    date_debut_activite: str | None = None
    date_immatriculation: str | None = None
    date_radiation: str | None = None
    duree_personne_morale: int | None = None
    date_fin_existence: str | None = None
    nature_entreprise: list | None = None
    date_cloture_exercice: str | None = None
    capital_social: float | None = None
    capital_variable: bool | None = None
    devise_capital: str | None = None
    indicateur_associe_unique: bool | None = None


class Complements(BaseModel):
    collectivite_territoriale: CollectiviteTerritoriale | None = None
    convention_collective_renseignee: bool = False
    liste_idcc: list | None = None
    liste_finess_juridique: list | None = None
    egapro_renseignee: bool = False
    est_achats_responsables: bool = False
    est_alim_confiance: bool = False
    est_association: bool = False
    est_bio: bool = False
    est_entrepreneur_individuel: bool = False
    est_entrepreneur_spectacle: bool = False
    est_ess: bool = False
    est_finess: bool = False
    est_organisme_formation: bool = False
    est_qualiopi: bool = False
    liste_id_organisme_formation: list | None = None
    est_rge: bool = False
    est_service_public: bool = False
    est_l100_3: bool = False
    est_siae: bool = False
    est_societe_mission: bool = False
    est_uai: bool = False
    est_patrimoine_vivant: bool = False
    bilan_ges_renseigne: bool = False
    identifiant_association: str | None = None
    statut_entrepreneur_spectacle: str | None = None
    type_siae: str | None = None


class UniteLegaleResponse(BaseModel):
    siren: str
    nom_complet: str | None = None
    nom_raison_sociale: str | None = None
    sigle: str | None = None
    nombre_etablissements: int | None = None
    nombre_etablissements_ouverts: int | None = None
    siege: Etablissement | None = None
    activite_principale: str | None = None
    categorie_entreprise: str | None = None
    caractere_employeur: str | None = None
    annee_categorie_entreprise: str | None = None
    date_creation: str | None = None
    date_fermeture: str | None = None
    date_mise_a_jour: str | None = None
    date_mise_a_jour_insee: str | None = None
    date_mise_a_jour_rne: str | None = None
    dirigeants: list[DirigeantsPP | DirigeantsPM] | None = None
    etat_administratif: str | None = None
    nature_juridique: str | None = None
    section_activite_principale: str | None = None
    tranche_effectif_salarie: str | None = None
    annee_tranche_effectif_salarie: str | None = None
    statut_diffusion: str | None = None
    matching_etablissements: list[Etablissement] | None = None
    etablissements: list[Etablissement] | None = None
    immatriculation: Immatriculation | None = None
    finances: dict[str, Finances] | None = None
    complements: Complements | None = None
    score: float | None = None
    slug: str | None = None
    meta: dict | None = None
