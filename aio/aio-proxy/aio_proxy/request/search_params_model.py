import re

from aio_proxy.labels.helpers import (
    codes_naf,
    departements,
    natures_juridiques,
    regions,
    sections_codes_naf,
    tranches_effectifs,
    valid_admin_fields_to_select,
    valid_fields_to_select,
)
from pydantic import BaseModel, validator

MAX_PAGE_VALUE = 1000
MIN_PAGE_NUMBER = 0
MIN_RADIUS = 0
MAX_RADIUS = 50


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
    matching_size: int = 10
    lat: float | None = None
    lon: float | None = None
    radius: float | None = 5
    minimal: bool | None = False
    include: list | None = None
    include_admin: list | None = None

    @validator("page", pre=True, always=True)
    def validate_page(cls, page):
        page = page - 1  # default 1
        # 1000 is elasticsearch's default page limit
        if page <= MIN_PAGE_NUMBER - 1 or page >= MAX_PAGE_VALUE:
            raise ValueError(
                "Veuillez indiquer un numéro de page entier entre 1 "
                "et 1000, par défaut 1."
            )
        return page

    @validator("per_page", pre=True, always=True)
    def validate_per_page(cls, per_page):
        max_per_page = 25
        min_per_page = 1
        if per_page > max_per_page or per_page < min_per_page:
            raise ValueError(
                "Veuillez indiquer un `per_page` entre 1 et 25, par défaut 10."
            )
        return per_page

    @validator("terms", pre=True, always=True)
    def validate_terms(cls, terms):
        if terms:
            return terms.upper()
        return terms

    @validator("matching_size", pre=True, always=True)
    def validate_matching_size(cls, matching_size):
        min_matching_size = 0
        max_matching_size = 100
        if matching_size <= min_matching_size or matching_size > max_matching_size:
            raise ValueError(
                "Veuillez indiquer un nombre d'établissements"
                "connexes entier entre 1 et "
                "100, par défaut 10."
            )
        return matching_size

    @validator("nature_juridique_unite_legale", pre=True, always=True)
    def validate_nature_juridique(cls, list_nature_juridique):
        for nature_juridique in list_nature_juridique:
            if nature_juridique not in natures_juridiques:
                raise ValueError(
                    f"Au moins une nature juridique est non valide. "
                    f"Les natures juridiques valides : "
                    f"{[nature_juridique for nature_juridique in natures_juridiques]}."
                )
        return list_nature_juridique

    @validator(
        "min_date_naiss_personne", "max_date_naiss_personne", pre=True, always=True
    )
    def validate_date(cls, date):
        return date.fromisoformat(date)

    @validator(
        "ca_min",
        "ca_max",
        "resultat_net_min",
        "resultat_net_max",
        pre=True,
        always=True,
    )
    def validate_long_int(cls, int_val):
        # Elasticsearch `long` type maxes out at this range
        min_val = -9223372036854775295
        max_val = 9223372036854775295

        if min_val <= int_val <= max_val:
            return int_val
        else:
            raise ValueError(
                f"Veuillez indiquer un entier entre {min_val} et {max_val}."
            )

    @validator("type_personne", pre=True, always=True)
    def validate_type_personne(cls, type_personne):
        if type_personne not in ["ELU", "DIRIGEANT"]:
            raise ValueError(
                "type_personne doit prendre la valeur 'dirigeant' ou 'elu' !"
            )
        return type_personne

    @validator("etat_administratif_unite_legale", pre=True, always=True)
    def validate_etat_administratif(cls, etat_administratif):
        if etat_administratif not in ["A", "C"]:
            raise ValueError("L'état administratif doit prendre la valeur 'A' ou 'C' !")
        return etat_administratif

    @validator("activite_principale_unite_legale", pre=True, always=True)
    def validate_activite_principale(cls, activite_principale_unite_legale):
        length_activite_principale = 6
        for activite_principale in activite_principale_unite_legale:
            if len(activite_principale) != length_activite_principale:
                raise ValueError(
                    "Chaque activité principale doit contenir 6 caractères."
                )
            if activite_principale not in codes_naf:
                raise ValueError("Au moins une des activités principales est inconnue.")
        return activite_principale_unite_legale

    @validator("categorie_entreprise", pre=True, always=True)
    def validate_categorie_entreprise(cls, list_categorie_entreprise):
        for categorie_entreprise in list_categorie_entreprise:
            if categorie_entreprise not in ["GE", "PME", "ETI"]:
                raise ValueError(
                    "Chaque catégorie d'entreprise doit prendre une de ces "
                    "valeurs 'GE', 'PME' ou 'ETI'."
                )
        return list_categorie_entreprise

    @validator("commune", pre=True, always=True)
    def validate_commune(cls, list_commune):
        length_code_commune = 5
        for code_commune in list_commune:
            if len(code_commune) != length_code_commune:
                raise ValueError("Chaque code commune doit contenir 5 caractères !")
            codes_valides = r"^([013-9]\d|2[AB1-9])\d{3}$"
            if not re.search(codes_valides, code_commune):
                raise ValueError("Au moins un des codes communes est non valide.")
        return list_commune

    @validator("code_postal", pre=True, always=True)
    def validate_code_postal(cls, list_code_postal):
        length_cod_postal = 5
        for code_postal in list_code_postal:
            if len(code_postal) != length_cod_postal:
                raise ValueError("Chaque code postal doit contenir 5 caractères !")
            codes_valides = "^((0[1-9])|([1-8][0-9])|(9[0-8])|(2A)|(2B))[0-9]{3}$"
            if not re.search(codes_valides, code_postal):
                raise ValueError("Au moins un code postal est non valide.")
        return list_code_postal

    @validator("departement", pre=True, always=True)
    def validate_departement(cls, list_departement):
        for departement in list_departement:
            if departement not in departements:
                raise ValueError(
                    f"Au moins un département est non valide."
                    f" Les départements valides"
                    f" : {[dep for dep in departements]}"
                )
        return list_departement

    @validator("region", pre=True, always=True)
    def validate_region(cls, list_region):
        for region in list_region:
            if region not in regions:
                raise ValueError(
                    f"Au moins une region est non valide."
                    f" Les région valides"
                    f" : {regions}"
                )
        return list_region

    @validator(
        "est_entrepreneur_individuel",
        "convention_collective_renseignee",
        "egapro_renseignee",
        "est_bio",
        "est_finess",
        "est_uai",
        "est_collectivite_territoriale",
        "est_entrepreneur_spectacle",
        "est_association",
        "est_organisme_formation",
        "est_qualiopi",
        "est_rge",
        "est_service_public",
        "est_societe_mission",
        "economie_sociale_solidaire_unite_legale",
        "minimal",
        pre=True,
        always=True,
    )
    def validate_bool(cls, bool, field):
        param_name = field.name
        if bool not in ["TRUE", "FALSE"]:
            raise ValueError(f"{param_name} doit prendre la valeur 'true' ou 'false' !")
        return bool == "TRUE"

    @validator("section_activite_principale", pre=True, always=True)
    def validate_section_activite_principale(cls, list_section_activite_principale):
        for section_activite_principale in list_section_activite_principale:
            if section_activite_principale not in sections_codes_naf:
                raise ValueError(
                    "Au moins une section d'activité principale est non valide."
                )
        return list_section_activite_principale

    @validator("tranche_effectif_salarie_unite_legale", pre=True, always=True)
    def validate_tranche_effectif_salarie(cls, list_tranche_effectif_salarie):
        length_tranche_effectif_salarie = 2
        for tranche_effectif_salarie in list_tranche_effectif_salarie:
            if len(tranche_effectif_salarie) != length_tranche_effectif_salarie:
                raise ValueError("Chaque tranche salariés doit contenir 2 caractères.")
            if tranche_effectif_salarie not in tranches_effectifs:
                raise ValueError("Au moins une tranche salariés est non valide.")
        return list_tranche_effectif_salarie

    @validator("id_convention_collective", pre=True, always=True)
    def validate_id_convention_collective(cls, id_convention_collective):
        length_convention_collective = 4
        if len(id_convention_collective) != length_convention_collective:
            raise ValueError(
                "L'identifiant de convention collective doit contenir 4 caractères."
            )
        return id_convention_collective

    @validator("id_finess", pre=True, always=True)
    def validate_id_finess(cls, id_finess):
        len_id_finess = 9
        if len(id_finess) != len_id_finess:
            raise ValueError("L'identifiant FINESS doit contenir 9 caractères.")
        return id_finess

    @validator("id_uai", pre=True, always=True)
    def validate_id_uai(cls, id_uai):
        length_id_uai = 8
        if len(id_uai) != length_id_uai:
            raise ValueError("L'identifiant UAI doit contenir 8 caractères.")
        return id_uai

    @validator("code_collectivite_territoriale", pre=True, always=True)
    def validate_code_collectivite_territoriale(cls, list_code_cc):
        min_len_code_collectivite_territoriale = 2
        for code_collectivite_territoriale in list_code_cc:
            if (
                len(code_collectivite_territoriale)
                < min_len_code_collectivite_territoriale
            ):
                raise ValueError(
                    "Chaque identifiant code insee d'une collectivité "
                    "territoriale doit contenir au moins 2 caractères."
                )
        return list_code_cc

    @validator("include", pre=True, always=True)
    def validate_include(cls, list_fields):
        valid_fields_to_check = valid_fields_to_select
        for field in list_fields:
            if field not in valid_fields_to_check:
                valid_fields_lowercase = [
                    field.lower() for field in valid_fields_to_check
                ]
                raise ValueError(
                    f"Au moins un champ à inclure est non valide. "
                    f"Les champs valides : {valid_fields_lowercase}."
                )
        return list_fields

    @validator("include_admin", pre=True, always=True)
    def validate_include_admin(cls, list_fields):
        valid_fields_to_check = valid_admin_fields_to_select
        for field in list_fields:
            if field not in valid_fields_to_check:
                valid_fields_lowercase = [
                    field.lower() for field in valid_fields_to_check
                ]
                raise ValueError(
                    f"Au moins un champ à inclure est non valide. "
                    f"Les champs valides : {valid_fields_lowercase}."
                )
        return list_fields

    @validator("lat", pre=True, always=True)
    def validate_lat(cls, lat):
        min_latitude = -90
        max_latitude = 90
        if lat == "nan":
            raise ValueError("Veuillez indiquer une latitude entre -90° et 90°.")
        try:
            lat = float(lat)
        except ValueError:
            raise ValueError("Veuillez indiquer une latitude entre -90° et 90°.")
        if lat > max_latitude or lat < min_latitude:
            raise ValueError("Veuillez indiquer une latitude entre -90° et 90°.")

    @validator("lon", pre=True, always=True)
    def validate_lon(cls, lon):
        min_longitude = -180
        max_longitude = 180
        if lon == "nan":
            raise ValueError("Veuillez indiquer une longitude entre -180° et 180°.")
        try:
            lon = float(lon)
        except ValueError:
            raise ValueError("Veuillez indiquer une longitude entre -180° et 180°.")
        if lon > max_longitude or lon < min_longitude:
            raise ValueError("Veuillez indiquer une longitude entre -180° et 180°.")
        return lon

    @validator("radius", pre=True, always=True)
    def validate_radius(cls, radius):
        if radius <= MIN_RADIUS or radius > MAX_RADIUS:
            raise ValueError(
                "Veuillez indiquer un radius entier ou flottant "
                "bentre 0 et 50 (en km)."
            )
        return radius
