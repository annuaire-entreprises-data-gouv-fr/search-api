from aio_proxy.labels.helpers import (
    CODES_NAF,
    DEPARTEMENTS,
    NATURES_JURIDIQUES,
    REGIONS,
    SECTIONS_CODES_NAF,
    TRANCHES_EFFECTIFS,
)

VALID_FIELDS_TO_SELECT = [
    "COMPLEMENTS",
    "DIRIGEANTS",
    "FINANCES",
    "SIEGE",
    "MATCHING_ETABLISSEMENTS",
]
VALID_ADMIN_FIELDS_TO_SELECT = [
    "ETABLISSEMENTS",
    "SCORE",
    "SLUG",
]

NUMERIC_FIELD_LIMITS = {
    "page": {"min": 1, "max": 1000, "default": 1, "alias": "page"},
    "page_etablissements": {
        "min": 1,
        "max": 1000,
        "default": 1,
        "alias": "page_etablissements",
    },
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
    "total_results": {"min": 0, "max": 10000},
}


VALID_FIELD_VALUES = {
    "nature_juridique_unite_legale": {
        "valid_values": NATURES_JURIDIQUES,
        "alias": "nature_juridique",
    },
    "categorie_entreprise": {
        "valid_values": ["GE", "PME", "ETI"],
        "alias": "categorie_entreprise",
    },
    "departement": {
        "valid_values": DEPARTEMENTS,
        "alias": "departement",
    },
    "tranche_effectif_salarie_unite_legale": {
        "valid_values": TRANCHES_EFFECTIFS,
        "alias": "tranche_effectif_salarie",
    },
    "section_activite_principale": {
        "valid_values": SECTIONS_CODES_NAF,
        "alias": "section_activite_principale",
    },
    "region": {
        "valid_values": REGIONS,
        "alias": "region",
    },
    "activite_principale_unite_legale": {
        "valid_values": CODES_NAF,
        "alias": "activite_principale",
    },
    "commune": {
        "valid_values": r"^([013-9]\d|2[AB1-9])\d{3}$",
        "alias": "commune",
    },
    "code_postal": {
        "valid_values": r"^((0[1-9])|([1-8][0-9])|(9[0-8])|(2A)|(2B))[0-9]{3}$",
        "alias": "activite_principale",
    },
    "type_personne": {
        "valid_values": ["ELU", "DIRIGEANT"],
        "alias": "type_personne",
    },
    "etat_administratif_unite_legale": {
        "valid_values": ["A", "C"],
        "alias": "etat_administratif",
    },
}

FIELD_LENGTHS = {
    "id_convention_collective": 4,
    "id_finess": 9,
    "id_uai": 8,
    "code_collectivite_territoriale": 2,
    "commune": 5,
    "code_postal": 5,
    "terms": 3,
}
