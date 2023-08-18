from dataclasses import dataclass


@dataclass
class UniteLegaleEtablissement:
    activite_principale: str = None
    activite_principale_registre_metier: str = None
    adresse: str = None
    cedex: str = None
    code_pays_etranger: str = None
    code_postal: str = None
    commune: str = None
    complement_adresse: str = None
    coordonnees: str = None
    date_creation: str = None
    date_debut_activite: str = None
    departement: str = None
    distribution_speciale: str = None
    est_siege: str = None
    etat_administratif: str = None
    geo_adresse: str = None
    geo_id: str = None
    indice_repetition: str = None
    latitude: str = None
    libelle_cedex: str = None
    libelle_commune: str = None
    libelle_commune_etranger: str = None
    libelle_pays_etranger: str = None
    libelle_voie: str = None
    liste_enseignes: list = None
    liste_finess: list = None
    liste_id_bio: list = None
    liste_idcc: list = None
    liste_id_organisme_formation: list = None
    liste_rge: list = None
    liste_uai: list = None
    longitude: str = None
    nom_commercial: str = None
    numero_voie: str = None
    region: str = None
    siret: str = None
    tranche_effectif_salarie: str = None
    type_voie: str = None


@dataclass
class UniteLegaleElu:
    nom: str = None
    prenoms: str = None
    annee_de_naissance: str = None
    fonction: str = None
    sexe: str = None


@dataclass
class UniteLegaleDirigeantsPM:
    siren: str = None
    denomination: str = None
    sigle: str = None
    qualite: str = None
    type_dirigeant: str = None


@dataclass
class UniteLegaleDirigeantsPP:
    nom: str = None
    prenoms: str = None
    annee_de_naissance: str = None
    qualite: str = None
    type_dirigeant: str = "personne physique"


@dataclass
class UniteLegaleDirigeant:
    dirigeants_pm: list[UniteLegaleDirigeantsPM]
    dirigeants_pp: list[UniteLegaleDirigeantsPP]


@dataclass
class UniteLegaleFinances:
    annee_cloture_exercice: int = None
    ca: int = None
    resultat_net: int = None


@dataclass
class UniteLegaleCollectiviteTerritoriale:
    code: str = None
    code_insee: str = None
    elus: list[UniteLegaleElu] = None
    niveau: str = None


@dataclass
class UniteLegaleComplements:
    collectivite_territoriale: UniteLegaleCollectiviteTerritoriale
    convention_collective_renseignee: str = None
    egapro_renseignee: str = None
    est_bio: str = None
    est_entrepreneur_individuel: str = None
    est_entrepreneur_spectacle: str = None
    est_ess: str = None
    est_finess: str = None
    est_organisme_formation: str = None
    est_qualiopi: str = None
    liste_id_organisme_formation: str = None
    est_rge: str = None
    est_service_public: str = None
    est_societe_mission: str = None
    est_uai: str = None
    identifiant_association: str = None
    statut_entrepreneur_spectacle: str = None


@dataclass
class UniteLegaleResponse:
    """Class for modelling unite légale response"""

    siren: str = None
    nom_complet: str = None
    nom_raison_sociale: str = None
    sigle: str = None
    nombre_etablissements: int = None
    nombre_etablissements_ouverts: int = None
    siege: UniteLegaleEtablissement = None
    activite_principale: str = None
    categorie_entreprise: str = None
    annee_categorie_entreprise: str = None
    date_creation: str = None
    date_mise_a_jour: str = None
    dirigeants: list[UniteLegaleDirigeantsPP] | list[UniteLegaleDirigeantsPM] = None
    etat_administratif: str = None
    nature_juridique: str = None
    section_activite_principale: str = None
    tranche_effectif_salarie: str = None
    annee_tranche_effectif_salarie: str = None
    statut_diffusion: str = None
    matching_etablissements: str = None
    etablissements: list[UniteLegaleEtablissement] = None
    finances: list[UniteLegaleFinances] = None
    complements: UniteLegaleComplements = None
    score: float = None
    slug: str = None
    meta: dict = None
