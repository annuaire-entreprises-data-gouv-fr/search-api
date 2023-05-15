from dataclasses import dataclass

from aio_proxy.parsers.activite_principale import validate_activite_principale
from aio_proxy.parsers.ban_params import ban_params
from aio_proxy.parsers.bool_fields import validate_bool_field
from aio_proxy.parsers.categorie_entreprise import validate_categorie_entreprise
from aio_proxy.parsers.code_commune import validate_code_commune
from aio_proxy.parsers.code_postal import validate_code_postal
from aio_proxy.parsers.collectivite_territoriale import (
    validate_code_collectivite_territoriale,
)
from aio_proxy.parsers.convention_collective import validate_id_convention_collective
from aio_proxy.parsers.date_parser import parse_and_validate_date, validate_date_range
from aio_proxy.parsers.departement import validate_departement
from aio_proxy.parsers.empty_params import check_empty_params
from aio_proxy.parsers.etat_administratif import validate_etat_administratif
from aio_proxy.parsers.finess import validate_id_finess
from aio_proxy.parsers.insee_bool import match_bool_to_insee_value
from aio_proxy.parsers.int_parser import parse_and_validate_int
from aio_proxy.parsers.latitude import parse_and_validate_latitude
from aio_proxy.parsers.list_parser import str_to_list
from aio_proxy.parsers.longitude import parse_and_validate_longitude
from aio_proxy.parsers.matching_size import parse_and_validate_matching_size
from aio_proxy.parsers.nature_juridique import validate_nature_juridique
from aio_proxy.parsers.page import parse_and_validate_page
from aio_proxy.parsers.per_page import parse_and_validate_per_page
from aio_proxy.parsers.radius import parse_and_validate_radius
from aio_proxy.parsers.rge import validate_id_rge
from aio_proxy.parsers.section_activite_principale import (
    validate_section_activite_principale,
)
from aio_proxy.parsers.string_parser import clean_parameter, parse_parameter
from aio_proxy.parsers.terms import (
    check_short_terms_and_no_param,
    parse_and_validate_terms,
)
from aio_proxy.parsers.tranche_effectif import validate_tranche_effectif_salarie
from aio_proxy.parsers.type_personne import validate_type_personne
from aio_proxy.parsers.uai import validate_id_uai


@dataclass
class SearchParams:
    page: int = None
    per_page: int = None
    terms: str = None
    activite_principale: list = None
    bilan_renseigne: str = None
    categorie_entreprise: list = None
    code_commune: list = None
    code_postal: list = None
    departement: list = None
    est_entrepreneur_individuel: str = None
    section_activite_principale: list = None
    tranche_effectif_salarie: list = None
    convention_collective_renseignee: str = None
    egapro_renseignee: str = None
    est_bio: str = None
    est_finess: str = None
    est_uai: str = None
    est_collectivite_territoriale: str = None
    est_entrepreneur_spectacle: str = None
    est_association: str = None
    est_organisme_formation: str = None
    est_qualiopi: str = None
    est_rge: str = None
    est_service_public: str = None
    est_societe_mission: str = None
    ess: str = None
    id_convention_collective: str = None
    id_finess: str = None
    id_uai: str = None
    code_collectivite_territoriale: str = None
    id_rge: str = None
    nom_personne: str = None
    prenoms_personne: str = None
    min_date_naiss_personne: str = None
    max_date_naiss_personne: str = None
    ca_min: str = None
    ca_max: str = None
    resultat_net_min: str = None
    resultat_net_max: str = None
    type_personne: str = None
    etat_administratif: str = None
    nature_juridique: list = None
    inclure_etablissements: bool = None
    inclure_slug: bool = None
    inclure_score: bool = None
    matching_size: str = None
    lat: float = None
    lon: float = None
    radius: float = None


class TextSearchParamsFactory:
    def __init__(self, request):
        self.params = SearchParams(
            page=parse_and_validate_page(request),
            per_page=parse_and_validate_per_page(request),
            terms=parse_and_validate_terms(request),
            matching_size=parse_and_validate_matching_size(request),
            inclure_score=validate_bool_field(
                "inclure_score",
                clean_parameter(request, param="inclure_score"),
            ),
            inclure_slug=validate_bool_field(
                "inclure_slug",
                clean_parameter(request, param="inclure_slug"),
            ),
            inclure_etablissements=validate_bool_field(
                "inclure_etablissements",
                clean_parameter(request, param="inclure_etablissements"),
            ),
            nature_juridique=validate_nature_juridique(
                str_to_list(clean_parameter(request, param="nature_juridique"))
            ),
            id_rge=validate_id_rge(clean_parameter(request, param="id_rge")),
            nom_personne=parse_parameter(request, param="nom_personne"),
            prenoms_personne=parse_parameter(request, param="prenoms_personne"),
            min_date_naiss_personne=parse_and_validate_date(
                request, param="date_naissance_personne_min"
            ),
            max_date_naiss_personne=parse_and_validate_date(
                request, param="date_naissance_personne_max"
            ),
            ca_min=parse_and_validate_int(request, param="ca_min"),
            ca_max=parse_and_validate_int(request, param="ca_max"),
            resultat_net_min=parse_and_validate_int(request, param="resultat_net_min"),
            resultat_net_max=parse_and_validate_int(request, param="resultat_net_max"),
            type_personne=validate_type_personne(
                clean_parameter(request, param="type_personne")
            ),
            etat_administratif=validate_etat_administratif(
                clean_parameter(request, param="etat_administratif")
            ),
            activite_principale=validate_activite_principale(
                str_to_list(clean_parameter(request, param="activite_principale"))
            ),
            bilan_renseigne=validate_bool_field(
                "bilan_renseigne",
                clean_parameter(request, param="bilan_renseigne"),
            ),
            categorie_entreprise=validate_categorie_entreprise(
                str_to_list(clean_parameter(request, param="categorie_entreprise"))
            ),
            code_commune=validate_code_commune(
                str_to_list(clean_parameter(request, param="code_commune"))
            ),
            code_postal=validate_code_postal(
                str_to_list(clean_parameter(request, param="code_postal"))
            ),
            departement=validate_departement(
                str_to_list(clean_parameter(request, param="departement"))
            ),
            est_entrepreneur_individuel=validate_bool_field(
                "est_entrepreneur_individuel",
                clean_parameter(request, param="est_entrepreneur_individuel"),
            ),
            section_activite_principale=validate_section_activite_principale(
                str_to_list(
                    clean_parameter(request, param="section_activite_principale")
                )
            ),
            tranche_effectif_salarie=validate_tranche_effectif_salarie(
                str_to_list(clean_parameter(request, param="tranche_effectif_salarie"))
            ),
            convention_collective_renseignee=validate_bool_field(
                "convention_collective_renseignee",
                clean_parameter(request, param="convention_collective_renseignee"),
            ),
            egapro_renseignee=validate_bool_field(
                "egapro_renseignee",
                clean_parameter(request, param="egapro_renseignee"),
            ),
            est_bio=validate_bool_field(
                "est_bio",
                clean_parameter(request, param="est_bio"),
            ),
            est_finess=validate_bool_field(
                "est_finess",
                clean_parameter(request, param="est_finess"),
            ),
            est_uai=validate_bool_field(
                "est_uai",
                clean_parameter(request, param="est_uai"),
            ),
            est_collectivite_territoriale=validate_bool_field(
                "est_collectivite_territoriale",
                clean_parameter(request, param="est_collectivite_territoriale"),
            ),
            est_entrepreneur_spectacle=validate_bool_field(
                "est_entrepreneur_spectacle",
                clean_parameter(request, param="est_entrepreneur_spectacle"),
            ),
            est_association=validate_bool_field(
                "est_association",
                clean_parameter(request, param="est_association"),
            ),
            est_organisme_formation=validate_bool_field(
                "est_organisme_formation",
                clean_parameter(request, param="est_organisme_formation"),
            ),
            est_qualiopi=validate_bool_field(
                "est_qualiopi",
                clean_parameter(request, param="est_qualiopi"),
            ),
            est_rge=validate_bool_field(
                "est_rge",
                clean_parameter(request, param="est_rge"),
            ),
            est_service_public=validate_bool_field(
                "est_service_public",
                clean_parameter(request, param="est_service_public"),
            ),
            est_societe_mission=match_bool_to_insee_value(
                validate_bool_field(
                    "est_societe_mission",
                    clean_parameter(request, param="est_societe_mission"),
                )
            ),
            ess=match_bool_to_insee_value(
                validate_bool_field(
                    "est_ess",
                    clean_parameter(request, param="est_ess"),
                )
            ),
            id_convention_collective=validate_id_convention_collective(
                clean_parameter(request, param="id_convention_collective")
            ),
            id_finess=validate_id_finess(clean_parameter(request, param="id_finess")),
            id_uai=validate_id_uai(clean_parameter(request, param="id_uai")),
            code_collectivite_territoriale=validate_code_collectivite_territoriale(
                str_to_list(
                    clean_parameter(request, param="code_collectivite_territoriale")
                )
            ),
        )
        self.check_and_validate_params(request)

    def check_and_validate_params(self, request):
        check_empty_params(self.params)
        ban_params(request, "localisation")
        validate_date_range(
            self.params.min_date_naiss_personne,
            self.params.max_date_naiss_personne,
        )
        # Prevent performance issues by refusing query terms less than 3 characters
        # unless another param is provided
        check_short_terms_and_no_param(self.params)


class GeoSearchParamsFactory:
    def __init__(self, request):
        self.params = SearchParams(
            page=parse_and_validate_page(request),
            per_page=parse_and_validate_per_page(request),
            lat=parse_and_validate_latitude(request),
            lon=parse_and_validate_longitude(request),
            radius=parse_and_validate_radius(request),
            activite_principale=validate_activite_principale(
                str_to_list(clean_parameter(request, param="activite_principale"))
            ),
            section_activite_principale=validate_section_activite_principale(
                str_to_list(
                    clean_parameter(request, param="section_activite_principale")
                )
            ),
            inclure_etablissements=validate_bool_field(
                "inclure_etablissements",
                clean_parameter(request, param="inclure_etablissements"),
            ),
            inclure_slug=validate_bool_field(
                "inclure_slug",
                clean_parameter(request, param="inclure_slug"),
            ),
            inclure_score=validate_bool_field(
                "inclure_score",
                clean_parameter(request, param="inclure_score"),
            ),
            matching_size=parse_and_validate_matching_size(request),
        )
