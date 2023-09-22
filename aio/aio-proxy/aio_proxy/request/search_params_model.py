import re
from datetime import date

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
from aio_proxy.request.parsers.insee_bool import match_bool_to_insee_value
from aio_proxy.request.parsers.string_parser import (
    clean_name,
    clean_parameter,
)
from aio_proxy.utils.utils import str_to_list
from pydantic import BaseModel, field_validator

FIELD_LIMITS = {
    "page": {"min": 1, "max": 1000, "default": 1, "alias": "page"},
    "per_page": {"min": 1, "max": 25, "default": 10, "alias": "per_page"},
    "matching_size": {
        "min": 1,
        "max": 100,
        "default": 10,
        "alias": "limite_matching_etablissements",
    },
    "ca_min": {
        "min": -9223372036854775295,
        "max": 9223372036854775295,
        "default": None,
        "alias": "ca_min",
    },
    "ca_max": {
        "min": -9223372036854775295,
        "max": 9223372036854775295,
        "default": None,
        "alias": "ca_max",
    },
    "resultat_net_min": {
        "min": -9223372036854775295,
        "max": 9223372036854775295,
        "default": None,
        "alias": "resultat_net_min",
    },
    "resultat_net_max": {
        "min": -9223372036854775295,
        "max": 9223372036854775295,
        "default": None,
        "alias": "resultat_net_max",
    },
    "lon": {"min": -180, "max": 180, "default": None, "alias": "longitude"},
    "lat": {"min": -90, "max": 90, "default": None, "alias": "latitude"},
    "radius": {"min": 0, "max": 50, "default": 5, "alias": "radius"},
}

FIELD_VALUES = {"type_personne": ["ELU", "DIRIGEANT"]}


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
    est_societe_mission: str | None = None
    economie_sociale_solidaire_unite_legale: str | None = None
    id_convention_collective: str | None = None
    id_finess: str | None = None
    id_uai: str | None = None
    code_collectivite_territoriale: str | None = None
    id_rge: str | None = None
    nom_personne: str | None = None
    prenoms_personne: str | None = None
    min_date_naiss_personne: date | None = None
    max_date_naiss_personne: date | None = None
    ca_min: int | None = None
    ca_max: int | None = None
    resultat_net_min: int | None = None
    resultat_net_max: int | None = None
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

    @field_validator("page", "per_page", "matching_size", mode="before")
    def validate_integer(cls, value, info):
        try:
            int(value)
        except ValueError:
            raise TypeError(f"Veuillez indiquer un `{info.field_name}` entier.")
        return int(value)

    @field_validator("radius", "lat", "lon", mode="before")
    def validate_float(cls, value, info):
        try:
            if value == "nan":
                raise ValueError
            float(value)
        except ValueError:
            raise TypeError(f"Veuillez indiquer un `{info.field_name}` flottant.")
        return float(value)

    @field_validator(
        "page", "per_page", "matching_size", "radius", "lat", "lon", mode="after"
    )
    def validate_number_range(cls, value, info):
        limits = FIELD_LIMITS.get(info.field_name)
        if int(value) < limits["min"] or int(value) > limits["max"]:
            raise TypeError(
                f"Veuillez indiquer un paramètre `{info.field_name}` entre"
                f"`{limits['min']}` et `{limits['max']}`,"
                f"par défaut `{limits['default']}`."
            )
        return value

    @field_validator("terms", mode="before")
    def make_uppercase(cls, terms):
        return terms.upper()

    @field_validator("nature_juridique_unite_legale", mode="before")
    def validate_nature_juridique(cls, nature_juridique):
        list_nature_juridique = str_to_list(clean_parameter(nature_juridique))
        for nature_juridique in list_nature_juridique:
            if nature_juridique not in natures_juridiques:
                raise TypeError(
                    f"Au moins une nature juridique est non valide. "
                    f"Les natures juridiques valides : "
                    f"{[nature_juridique for nature_juridique in natures_juridiques]}."
                )
        return list_nature_juridique

    @field_validator("nom_personne", "prenoms_personne", mode="before")
    def validate_nom(cls, nom):
        return clean_name(nom)

    @field_validator(
        "min_date_naiss_personne", "max_date_naiss_personne", mode="before"
    )
    def validate_date(cls, date_string):
        try:
            return date.fromisoformat(date_string)
        except Exception:
            raise TypeError(
                "Veuillez indiquer une date sous"
                "le format : aaaa-mm-jj. Exemple : '1990-01-02'"
            )

    @field_validator("type_personne", mode="before")
    def validate_type_personne(cls, type_personne):
        if type_personne.upper() not in ["ELU", "DIRIGEANT"]:
            raise TypeError(
                "type_personne doit prendre la valeur 'dirigeant' ou 'elu' !"
            )
        return type_personne.upper()

    @field_validator("etat_administratif_unite_legale", mode="before")
    def validate_etat_administratif(cls, etat_administratif):
        if etat_administratif.upper() not in ["A", "C"]:
            raise TypeError("L'état administratif doit prendre la valeur 'A' ou 'C' !")
        return etat_administratif

    @field_validator("activite_principale_unite_legale", mode="before")
    def validate_activite_principale(cls, activite_principale_unite_legale):
        list_activite_principale = str_to_list(
            clean_parameter(activite_principale_unite_legale)
        )
        length_activite_principale = 6
        for activite_principale in list_activite_principale:
            if len(activite_principale) != length_activite_principale:
                raise TypeError(
                    "Chaque activité principale doit contenir 6 caractères."
                )
            if activite_principale not in codes_naf:
                raise TypeError("Au moins une des activités principales est inconnue.")
        return list_activite_principale

    @field_validator("categorie_entreprise", mode="before")
    def validate_categorie_entreprise(cls, categorie_entreprise):
        list_categorie_entreprise = str_to_list(clean_parameter(categorie_entreprise))
        for categorie_entreprise in list_categorie_entreprise:
            if categorie_entreprise not in ["GE", "PME", "ETI"]:
                raise TypeError(
                    "Chaque catégorie d'entreprise doit prendre une de ces "
                    "valeurs 'GE', 'PME' ou 'ETI'."
                )
        return list_categorie_entreprise

    @field_validator("commune", mode="before")
    def validate_commune(cls, commune):
        list_commune = str_to_list(clean_parameter(commune))
        length_code_commune = 5
        for code_commune in list_commune:
            if len(code_commune) != length_code_commune:
                raise TypeError("Chaque code commune doit contenir 5 caractères !")
            codes_valides = r"^([013-9]\d|2[AB1-9])\d{3}$"
            if not re.search(codes_valides, code_commune):
                raise TypeError("Au moins un des codes communes est non valide.")
        return list_commune  # todo : separate validators

    @field_validator("code_postal", mode="before")
    def validate_code_postal(cls, code_postal):
        list_code_postal = str_to_list(clean_parameter(code_postal))
        length_cod_postal = 5
        for code_postal in list_code_postal:
            if len(code_postal) != length_cod_postal:
                raise TypeError("Chaque code postal doit contenir 5 caractères !")
            codes_valides = "^((0[1-9])|([1-8][0-9])|(9[0-8])|(2A)|(2B))[0-9]{3}$"
            if not re.search(codes_valides, code_postal):
                raise TypeError("Au moins un code postal est non valide.")
        return list_code_postal

    @field_validator("departement", mode="before")
    def validate_departement(cls, departement):
        list_departement = str_to_list(clean_parameter(departement))
        for departement in list_departement:
            if departement not in departements:
                raise TypeError(
                    f"Au moins un département est non valide."
                    f" Les départements valides"
                    f" : {[dep for dep in departements]}"
                )
        return list_departement

    @field_validator("region", mode="before")
    def validate_region(cls, region):
        list_region = str_to_list(clean_parameter(region))
        for region in list_region:
            if region not in regions:
                raise TypeError(
                    f"Au moins une region est non valide."
                    f" Les région valides"
                    f" : {regions}"
                )
        return list_region

    @field_validator(
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
        "minimal",
        mode="before",
    )
    def validate_bool(cls, boolean, info):
        param_name = info.field_name
        if boolean.upper() not in ["TRUE", "FALSE"]:
            raise TypeError(f"{param_name} doit prendre la valeur 'true' ou 'false' !")
        return boolean.upper() == "TRUE"

    @field_validator(
        "est_societe_mission", "economie_sociale_solidaire_unite_legale", mode="before"
    )
    def validate_societe_a_mission(cls, boolean, info):
        param_name = info.field_name
        if boolean.upper() not in ["TRUE", "FALSE"]:
            # Using TypeError because it is not wrapped in a Validation Error
            # in Pydantic
            raise TypeError(f"{param_name} doit prendre la valeur 'true' ou 'false' !")
        return match_bool_to_insee_value(boolean.upper() == "TRUE")

    @field_validator("section_activite_principale", mode="before")
    def validate_section_activite_principale(cls, section_activite_principale):
        list_section_activite_principale = str_to_list(
            clean_parameter(section_activite_principale)
        )
        for section_activite_principale in list_section_activite_principale:
            if section_activite_principale not in sections_codes_naf:
                raise TypeError(
                    "Au moins une section d'activité principale est non valide."
                )
        return list_section_activite_principale

    @field_validator("tranche_effectif_salarie_unite_legale", mode="before")
    def validate_tranche_effectif_salarie(cls, tranche_effectif_salarie):
        list_tranche_effectif_salarie = str_to_list(
            clean_parameter(tranche_effectif_salarie)
        )
        length_tranche_effectif_salarie = 2
        for tranche_effectif_salarie in list_tranche_effectif_salarie:
            if len(tranche_effectif_salarie) != length_tranche_effectif_salarie:
                raise TypeError("Chaque tranche salariés doit contenir 2 caractères.")
            if tranche_effectif_salarie not in tranches_effectifs:
                raise TypeError("Au moins une tranche salariés est non valide.")
        return list_tranche_effectif_salarie

    @field_validator("id_convention_collective", mode="before")
    def validate_id_convention_collective(cls, id_convention_collective):
        length_convention_collective = 4
        if len(id_convention_collective) != length_convention_collective:
            raise TypeError(
                "L'identifiant de convention collective doit contenir 4 caractères."
            )
        return id_convention_collective

    @field_validator("id_finess", mode="before")
    def validate_id_finess(cls, id_finess):  # *kwargs {'id_fitness' : id_fitness}
        len_id_finess = 9
        if len(id_finess) != len_id_finess:
            raise TypeError("L'identifiant FINESS doit contenir 9 caractères.")
        return id_finess

    @field_validator("id_uai", mode="before")
    def validate_id_uai(cls, id_uai):
        length_id_uai = 8
        if len(id_uai) != length_id_uai:
            raise TypeError("L'identifiant UAI doit contenir 8 caractères.")
        return id_uai

    @field_validator("code_collectivite_territoriale", mode="before")
    def validate_code_collectivite_territoriale(cls, code_cc):
        list_code_cc = str_to_list(clean_parameter(code_cc))
        min_len_code_collectivite_territoriale = 2
        for code_collectivite_territoriale in list_code_cc:
            if (
                len(code_collectivite_territoriale)
                < min_len_code_collectivite_territoriale
            ):
                raise TypeError(
                    "Chaque identifiant code insee d'une collectivité "
                    "territoriale doit contenir au moins 2 caractères."
                )
        return list_code_cc

    @field_validator("include", "include_admin", mode="before")
    def validate_include(cls, fields, info):
        list_fields = str_to_list(clean_parameter(fields))
        if info.field_name == "include_admin":
            valid_fields_to_check = valid_admin_fields_to_select
        else:
            valid_fields_to_check = valid_fields_to_select
        for field in list_fields:
            if field not in valid_fields_to_check:
                valid_fields_lowercase = [
                    field.lower() for field in valid_fields_to_check
                ]
                raise TypeError(
                    f"Au moins un champ à inclure est non valide. "
                    f"Les champs valides : {valid_fields_lowercase}."
                )
        return list_fields
