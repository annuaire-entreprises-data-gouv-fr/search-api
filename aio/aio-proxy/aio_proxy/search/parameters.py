from aio_proxy.parsers.activite_principale import validate_activite_principale
from aio_proxy.parsers.ban_params import ban_params
from aio_proxy.parsers.bool_fields import validate_bool_field
from aio_proxy.parsers.code_commune import validate_code_commune
from aio_proxy.parsers.code_postal import validate_code_postal
from aio_proxy.parsers.collectivite_territoriale import (
    validate_code_collectivite_territoriale,
)
from aio_proxy.parsers.convention_collective import validate_id_convention_collective
from aio_proxy.parsers.date_parser import parse_and_validate_date, validate_date_range
from aio_proxy.parsers.departement import validate_departement
from aio_proxy.parsers.empty_params import check_empty_params
from aio_proxy.parsers.ess import match_ess_bool_to_value
from aio_proxy.parsers.etat_administratif import validate_etat_administratif
from aio_proxy.parsers.finess import validate_id_finess
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


def extract_text_parameters(
    request,
) -> tuple[dict[str, str | None | bool | list], int, int]:
    """Extract all parameters from request.

    Args:
        request: request object.

    Returns:
        terms (str): full text search query.
        page (int): page number.
        per_page (int): number of results per page.
        filters (dict): key/value pairs containing filter values.

    Raises:
        HTTPBadRequest: if ValueError or KeyError raised.
    """
    ban_params(request, "localisation")
    page = parse_and_validate_page(request)
    per_page = parse_and_validate_per_page(request)
    terms = parse_and_validate_terms(request)
    activite_principale = validate_activite_principale(
        str_to_list(clean_parameter(request, param="activite_principale"))
    )
    code_commune = validate_code_commune(
        str_to_list(clean_parameter(request, param="code_commune"))
    )
    code_postal = validate_code_postal(
        str_to_list(clean_parameter(request, param="code_postal"))
    )
    departement = validate_departement(
        str_to_list(clean_parameter(request, param="departement"))
    )
    est_entrepreneur_individuel = validate_bool_field(
        "est_entrepreneur_individuel",
        clean_parameter(request, param="est_entrepreneur_individuel"),
    )
    section_activite_principale = validate_section_activite_principale(
        str_to_list(clean_parameter(request, param="section_activite_principale"))
    )
    tranche_effectif_salarie = validate_tranche_effectif_salarie(
        str_to_list(clean_parameter(request, param="tranche_effectif_salarie"))
    )
    convention_collective_renseignee = validate_bool_field(
        "convention_collective_renseignee",
        clean_parameter(request, param="convention_collective_renseignee"),
    )
    est_bio = validate_bool_field(
        "est_bio",
        clean_parameter(request, param="est_bio"),
    )
    est_finess = validate_bool_field(
        "est_finess",
        clean_parameter(request, param="est_finess"),
    )
    est_uai = validate_bool_field(
        "est_uai",
        clean_parameter(request, param="est_uai"),
    )
    est_collectivite_territoriale = validate_bool_field(
        "est_collectivite_territoriale",
        clean_parameter(request, param="est_collectivite_territoriale"),
    )
    est_entrepreneur_spectacle = validate_bool_field(
        "est_entrepreneur_spectacle",
        clean_parameter(request, param="est_entrepreneur_spectacle"),
    )
    est_association = validate_bool_field(
        "est_association",
        clean_parameter(request, param="est_association"),
    )
    est_organisme_formation = validate_bool_field(
        "est_organisme_formation",
        clean_parameter(request, param="est_organisme_formation"),
    )
    est_rge = validate_bool_field(
        "est_rge",
        clean_parameter(request, param="est_rge"),
    )
    est_service_public = validate_bool_field(
        "est_service_public",
        clean_parameter(request, param="est_service_public"),
    )
    ess = match_ess_bool_to_value(
        validate_bool_field(
            "est_ess",
            clean_parameter(request, param="est_ess"),
        )
    )
    id_convention_collective = validate_id_convention_collective(
        clean_parameter(request, param="id_convention_collective")
    )
    id_finess = validate_id_finess(clean_parameter(request, param="id_finess"))
    id_uai = validate_id_uai(clean_parameter(request, param="id_uai"))
    code_collectivite_territoriale = validate_code_collectivite_territoriale(
        str_to_list(clean_parameter(request, param="code_collectivite_territoriale"))
    )
    id_rge = validate_id_rge(clean_parameter(request, param="id_rge"))
    nom_personne = parse_parameter(request, param="nom_personne")
    prenoms_personne = parse_parameter(request, param="prenoms_personne")
    min_date_naiss_personne = parse_and_validate_date(
        request, param="date_naissance_personne_min"
    )
    max_date_naiss_personne = parse_and_validate_date(
        request, param="date_naissance_personne_max"
    )
    type_personne = validate_type_personne(
        clean_parameter(request, param="type_personne")
    )
    etat_administratif = validate_etat_administratif(
        clean_parameter(request, param="etat_administratif")
    )
    nature_juridique = validate_nature_juridique(
        str_to_list(clean_parameter(request, param="nature_juridique"))
    )

    inclure_etablissements = validate_bool_field(
        "inclure_etablissements",
        clean_parameter(request, param="inclure_etablissements"),
    )

    matching_size = parse_and_validate_matching_size(request)

    validate_date_range(min_date_naiss_personne, max_date_naiss_personne)

    parameters = {
        "terms": terms,
        "activite_principale_unite_legale": activite_principale,
        "commune": code_commune,
        "code_postal": code_postal,
        "departement": departement,
        "section_activite_principale": section_activite_principale,
        "tranche_effectif_salarie_unite_legale": tranche_effectif_salarie,
        "convention_collective_renseignee": convention_collective_renseignee,
        "etat_administratif_unite_legale": etat_administratif,
        "est_entrepreneur_individuel": est_entrepreneur_individuel,
        "est_association": est_association,
        "est_uai": est_uai,
        "est_finess": est_finess,
        "est_bio": est_bio,
        "est_collectivite_territoriale": est_collectivite_territoriale,
        "est_entrepreneur_spectacle": est_entrepreneur_spectacle,
        "est_organisme_formation": est_organisme_formation,
        "est_rge": est_rge,
        "est_service_public": est_service_public,
        "economie_sociale_solidaire_unite_legale": ess,
        "id_convention_collective": id_convention_collective,
        "id_finess": id_finess,
        "id_uai": id_uai,
        "id_rge": id_rge,
        "inclure_etablissements": inclure_etablissements,
        "code_collectivite_territoriale": code_collectivite_territoriale,
        "nom_personne": nom_personne,
        "prenoms_personne": prenoms_personne,
        "min_date_naiss_personne": min_date_naiss_personne,
        "max_date_naiss_personne": max_date_naiss_personne,
        "type_personne": type_personne,
        "matching_size": matching_size,
        "nature_juridique_unite_legale": nature_juridique,
    }

    # Check if at least one param has been provided in the request
    # It is easier to do it by checking if the param dict has only None values rather
    # than parse the request to check
    check_empty_params(parameters)

    # Prevent performance issues by refusing query terms less than 3 characters
    # unless another param is provided
    check_short_terms_and_no_param(parameters)

    return parameters, page, per_page


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
    matching_size = parse_and_validate_matching_size(request)
    parameters = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "activite_principale_unite_legale": activite_principale,
        "section_activite_principale": section_activite_principale,
        "inclure_etablissements": inclure_etablissements,
        "matching_size": matching_size,
    }
    return parameters, page, per_page
