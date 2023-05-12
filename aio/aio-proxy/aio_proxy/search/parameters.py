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
)
from aio_proxy.parsers.tranche_effectif import validate_tranche_effectif_salarie
from aio_proxy.parsers.type_personne import validate_type_personne
from aio_proxy.parsers.uai import validate_id_uai


class SearchParams:
    def __init__(self, request):
        self._page = None
        self._per_page = None
        self._terms = None
        self._activite_principale = None
        self._bilan_renseigne = None
        self._categorie_entreprise = None
        self._code_commune = None
        self._code_postal = None
        self._departement = None
        self._est_entrepreneur_individuel = None
        self._section_activite_principale = None
        self._tranche_effectif_salarie = None
        self._convention_collective_renseignee = None
        self._egapro_renseignee = None
        self._est_bio = None
        self._est_finess = None
        self._est_uai = None
        self._est_collectivite_territoriale = None
        self._est_entrepreneur_spectacle = None
        self._est_association = None
        self._est_organisme_formation = None
        self._est_qualiopi = None
        self._est_rge = None
        self._est_service_public = None
        self._est_societe_mission = None
        self._ess = None
        self._id_convention_collective = None
        self._id_finess = None
        self._id_uai = None
        self._code_collectivite_territoriale = None
        self._id_rge = None
        self._nom_personne = None
        self._prenoms_personne = None
        self._min_date_naiss_personne = None
        self._max_date_naiss_personne = None
        self._ca_min = None
        self._ca_max = None
        self._resultat_net_min = None
        self._resultat_net_max = None
        self._type_personne = None
        self._etat_administratif = None
        self._nature_juridique = None
        self._inclure_etablissements = False
        self._inclure_slug = False
        self._inclure_score = False
        self._matching_size = None
        self.check_and_validate_params(request)

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, request):
        self._page = parse_and_validate_page(request)

    @property
    def per_page(self):
        return self._per_page

    @per_page.setter
    def per_page(self, request):
        self._per_page = parse_and_validate_per_page(request)

    @property
    def matching_size(self):
        return self._matching_size

    @matching_size.setter
    def matching_size(self, request):
        self._matching_size = parse_and_validate_matching_size(request)

    @property
    def inclure_score(self):
        return self._inclure_score

    @inclure_score.setter
    def inclure_score(self, request):
        self._inclure_score = validate_bool_field(
            "inclure_score",
            clean_parameter(request, param="inclure_score"),
        )

    @property
    def inclure_slug(self):
        return self._inclure_slug

    @inclure_slug.setter
    def inclure_slug(self, request):
        self._inclure_slug = validate_bool_field(
            "inclure_slug",
            clean_parameter(request, param="inclure_slug"),
        )

    @property
    def inclure_etablissements(self):
        return self._inclure_etablissements

    @inclure_etablissements.setter
    def inclure_etablissements(self, request):
        self._inclure_etablissements = validate_bool_field(
            "inclure_etablissements",
            clean_parameter(request, param="inclure_etablissements"),
        )

    @property
    def nature_juridique(self):
        return self._nature_juridique

    @nature_juridique.setter
    def nature_juridique(self, request):
        self._nature_juridique = validate_nature_juridique(
            str_to_list(clean_parameter(request, param="nature_juridique"))
        )

    @property
    def id_rge(self):
        return self._id_rge

    @id_rge.setter
    def id_rge(self, request):
        self._id_rge = validate_id_rge(clean_parameter(request, param="id_rge"))

    @property
    def nom_personne(self):
        return self._nom_personne

    @nom_personne.setter
    def nom_personne(self, request):
        self._nom_personne = parse_parameter(request, param="nom_personne")

    @property
    def prenoms_personne(self):
        return self._prenoms_personne

    @prenoms_personne.setter
    def prenoms_personne(self, request):
        self._prenoms_personne = parse_parameter(request, param="prenoms_personne")

    @property
    def min_date_naiss_personne(self):
        return self._min_date_naiss_personne

    @min_date_naiss_personne.setter
    def min_date_naiss_personne(self, request):
        self._min_date_naiss_personne = parse_and_validate_date(
            request, param="date_naissance_personne_min"
        )

    @property
    def max_date_naiss_personne(self):
        return self._max_date_naiss_personne

    @max_date_naiss_personne.setter
    def max_date_naiss_personne(self, request):
        self._max_date_naiss_personne = parse_and_validate_date(
            request, param="date_naissance_personne_max"
        )

    @property
    def ca_min(self):
        return self._ca_min

    @ca_min.setter
    def ca_min(self, request):
        self._ca_min = parse_and_validate_int(request, param="ca_min")

    @property
    def ca_max(self):
        return self._ca_max

    @ca_max.setter
    def ca_max(self, request):
        self._ca_max = parse_and_validate_int(request, param="ca_max")

    @property
    def resultat_net_min(self):
        return self._resultat_net_min

    @resultat_net_min.setter
    def resultat_net_min(self, request):
        self._resultat_net_min = parse_and_validate_int(
            request, param="resultat_net_min"
        )

    @property
    def resultat_net_max(self):
        return self._resultat_net_max

    @resultat_net_max.setter
    def resultat_net_max(self, request):
        self._resultat_net_max = parse_and_validate_int(
            request, param="resultat_net_max"
        )

    @property
    def type_personne(self):
        return self._type_personne

    @type_personne.setter
    def type_personne(self, request):
        self._type_personne = validate_type_personne(
            clean_parameter(request, param="type_personne")
        )

    @property
    def etat_administratif(self):
        return self._etat_administratif

    @etat_administratif.setter
    def etat_administratif(self, request):
        self._etat_administratif = validate_etat_administratif(
            clean_parameter(request, param="etat_administratif")
        )

    @property
    def activite_principale(self):
        return self._activite_principale

    @activite_principale.setter
    def activite_principale(self, request):
        self._activite_principale = validate_activite_principale(
            str_to_list(clean_parameter(request, param="activite_principale"))
        )

    @property
    def bilan_renseigne(self):
        return self._bilan_renseigne

    @bilan_renseigne.setter
    def bilan_renseigne(self, request):
        self._bilan_renseigne = validate_bool_field(
            "bilan_renseigne",
            clean_parameter(request, param="bilan_renseigne"),
        )

    @property
    def categorie_entreprise(self):
        return self._categorie_entreprise

    @categorie_entreprise.setter
    def categorie_entreprise(self, request):
        self._categorie_entreprise = validate_categorie_entreprise(
            str_to_list(clean_parameter(request, param="categorie_entreprise"))
        )

    @property
    def code_commune(self):
        return self._code_commune

    @code_commune.setter
    def code_commune(self, request):
        self._code_commune = validate_code_commune(
            str_to_list(clean_parameter(request, param="code_commune"))
        )

    @property
    def code_postal(self):
        return self._code_postal

    @code_postal.setter
    def code_postal(self, request):
        self._code_postal = validate_code_postal(
            str_to_list(clean_parameter(request, param="code_postal"))
        )

    @property
    def departement(self):
        return self._departement

    @departement.setter
    def departement(self, request):
        self._departement = validate_departement(
            str_to_list(clean_parameter(request, param="departement"))
        )

    @property
    def est_entrepreneur_individuel(self):
        return self._est_entrepreneur_individuel

    @est_entrepreneur_individuel.setter
    def est_entrepreneur_individuel(self, request):
        self._est_entrepreneur_individuel = validate_bool_field(
            "est_entrepreneur_individuel",
            clean_parameter(request, param="est_entrepreneur_individuel"),
        )

    @property
    def section_activite_principale(self):
        return self._section_activite_principale

    @section_activite_principale.setter
    def section_activite_principale(self, request):
        self._section_activite_principale = validate_section_activite_principale(
            str_to_list(clean_parameter(request, param="section_activite_principale"))
        )

    @property
    def tranche_effectif_salarie(self):
        return self._tranche_effectif_salarie

    @tranche_effectif_salarie.setter
    def tranche_effectif_salarie(self, request):
        self._tranche_effectif_salarie = validate_tranche_effectif_salarie(
            str_to_list(clean_parameter(request, param="tranche_effectif_salarie"))
        )

    @property
    def convention_collective_renseignee(self):
        return self._convention_collective_renseignee

    @convention_collective_renseignee.setter
    def convention_collective_renseignee(self, request):
        self._convention_collective_renseignee = validate_bool_field(
            "convention_collective_renseignee",
            clean_parameter(request, param="convention_collective_renseignee"),
        )

    @property
    def egapro_renseignee(self):
        return self._egapro_renseignee

    @egapro_renseignee.setter
    def egapro_renseignee(self, request):
        self._egapro_renseignee = validate_bool_field(
            "egapro_renseignee",
            clean_parameter(request, param="egapro_renseignee"),
        )

    @property
    def est_bio(self):
        return self._est_bio

    @est_bio.setter
    def est_bio(self, request):
        self._st_bio = validate_bool_field(
            "est_bio",
            clean_parameter(request, param="est_bio"),
        )

    @property
    def est_finess(self):
        return self._est_finess

    @est_finess.setter
    def est_finess(self, request):
        self._est_finess = validate_bool_field(
            "est_finess",
            clean_parameter(request, param="est_finess"),
        )

    @property
    def est_uai(self):
        return self._est_uai

    @est_uai.setter
    def est_uai(self, request):
        self._est_uai = validate_bool_field(
            "est_uai",
            clean_parameter(request, param="est_uai"),
        )

    @property
    def est_collectivite_territoriale(self):
        return self._est_collectivite_territoriale

    @est_collectivite_territoriale.setter
    def est_collectivite_territoriale(self, request):
        self._est_collectivite_territoriale = validate_bool_field(
            "est_collectivite_territoriale",
            clean_parameter(request, param="est_collectivite_territoriale"),
        )

    @property
    def est_entrepreneur_spectacle(self):
        return self._est_entrepreneur_spectacle

    @est_entrepreneur_spectacle.setter
    def est_entrepreneur_spectacle(self, request):
        self._est_entrepreneur_spectacle = validate_bool_field(
            "est_entrepreneur_spectacle",
            clean_parameter(request, param="est_entrepreneur_spectacle"),
        )

    @property
    def est_association(self):
        return self._est_association

    @est_association.setter
    def est_association(self, request):
        self.est_association = validate_bool_field(
            "est_association",
            clean_parameter(request, param="est_association"),
        )

    @property
    def est_organisme_formation(self):
        return self._est_organisme_formation

    @est_organisme_formation.setter
    def est_organisme_formation(self, request):
        self._est_organisme_formation = validate_bool_field(
            "est_organisme_formation",
            clean_parameter(request, param="est_organisme_formation"),
        )

    @property
    def est_qualiopi(self):
        return self._est_qualiopi

    @est_qualiopi.setter
    def est_qualiopi(self, request):
        self.est_qualiopi = validate_bool_field(
            "est_qualiopi",
            clean_parameter(request, param="est_qualiopi"),
        )

    @property
    def est_rge(self):
        return self._est_rge

    @est_rge.setter
    def est_rge(self, request):
        self.est_rge = validate_bool_field(
            "est_rge",
            clean_parameter(request, param="est_rge"),
        )

    @property
    def est_service_public(self):
        return self._est_service_public

    @est_service_public.setter
    def est_service_public(self, request):
        self._est_service_public = validate_bool_field(
            "est_service_public",
            clean_parameter(request, param="est_service_public"),
        )

    @property
    def est_societe_mission(self):
        return self._est_societe_mission

    @est_societe_mission.setter
    def est_societe_mission(self, request):
        self._est_societe_mission = match_bool_to_insee_value(
            validate_bool_field(
                "est_societe_mission",
                clean_parameter(request, param="est_societe_mission"),
            )
        )

    @property
    def ess(self):
        return self._ess

    @ess.setter
    def ess(self, request):
        self._ess = match_bool_to_insee_value(
            validate_bool_field(
                "est_ess",
                clean_parameter(request, param="est_ess"),
            )
        )

    @property
    def id_convention_collective(self):
        return self._id_convention_collective

    @id_convention_collective.setter
    def id_convention_collective(self, request):
        self._id_convention_collective = validate_id_convention_collective(
            clean_parameter(request, param="id_convention_collective")
        )

    @property
    def id_finess(self):
        return self._id_finess

    @id_finess.setter
    def id_finess(self, request):
        self._id_finess = validate_id_finess(
            clean_parameter(request, param="id_finess")
        )

    @property
    def id_uai(self):
        return self._id_uai

    @id_uai.setter
    def id_uai(self, request):
        self._id_uai = validate_id_uai(clean_parameter(request, param="id_uai"))

    @property
    def code_collectivite_territoriale(self):
        return self._code_collectivite_territoriale

    @code_collectivite_territoriale.setter
    def code_collectivite_territoriale(self, request):
        self._code_collectivite_territoriale = validate_code_collectivite_territoriale(
            str_to_list(
                clean_parameter(request, param="code_collectivite_territoriale")
            )
        )

    def check_and_validate_params(self, request):
        check_empty_params(self)
        ban_params(request, "localisation")
        validate_date_range(
            self._min_date_naiss_personne, self._max_date_naiss_personne
        )
        # Prevent performance issues by refusing query terms less than 3 characters
        # unless another param is provided
        check_short_terms_and_no_param(self)


def extract_geo_parameters(request):
    page = parse_and_validate_page(request)
    per_page = parse_and_validate_per_page(request)
    lat = parse_and_validate_latitude(request)
    lon = parse_and_validate_longitude(request)
    radius = parse_and_validate_radius(request)
    activite_principale = validate_activite_principale(
        str_to_list(clean_parameter(request, param="activite_principale"))
    )
    section_activite_principale = validate_section_activite_principale(
        str_to_list(clean_parameter(request, param="section_activite_principale"))
    )
    inclure_etablissements = validate_bool_field(
        "inclure_etablissements",
        clean_parameter(request, param="inclure_etablissements"),
    )
    inclure_slug = validate_bool_field(
        "inclure_slug",
        clean_parameter(request, param="inclure_slug"),
    )
    inclure_score = validate_bool_field(
        "inclure_score",
        clean_parameter(request, param="inclure_score"),
    )
    matching_size = parse_and_validate_matching_size(request)
    parameters = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "activite_principale_unite_legale": activite_principale,
        "section_activite_principale": section_activite_principale,
        "inclure_etablissements": inclure_etablissements,
        "matching_size": matching_size,
        "inclure_slug": inclure_slug,
        "inclure_score": inclure_score,
    }
    return parameters, page, per_page
