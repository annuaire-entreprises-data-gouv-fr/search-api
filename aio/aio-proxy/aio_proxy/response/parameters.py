from typing import Dict, Tuple, Union

from aio_proxy.parsers.activite_principale import validate_activite_principale
from aio_proxy.parsers.code_postal import validate_code_postal
from aio_proxy.parsers.colter_code_insee import validate_colter_code_insee
from aio_proxy.parsers.date_parser import parse_and_validate_date, validate_date_range
from aio_proxy.parsers.departement import validate_departement
from aio_proxy.parsers.empty_params import check_empty_params
from aio_proxy.parsers.entrepreneur_individuel import (
    validate_is_entrepreneur_individuel,
)
from aio_proxy.parsers.finess import validate_finess
from aio_proxy.parsers.exist_fields import validate_is_field
from aio_proxy.parsers.idcc import validate_idcc
from aio_proxy.parsers.latitude import parse_and_validate_latitude
from aio_proxy.parsers.longitude import parse_and_validate_longitude
from aio_proxy.parsers.page import parse_and_validate_page
from aio_proxy.parsers.per_page import parse_and_validate_per_page
from aio_proxy.parsers.radius import parse_and_validate_radius
from aio_proxy.parsers.section_activite_principale import (
    validate_section_activite_principale,
)
from aio_proxy.parsers.string_parser import clean_parameter, parse_parameter
from aio_proxy.parsers.terms import (
    check_no_param_and_length_terms,
    parse_and_validate_terms,
)
from aio_proxy.parsers.uai import validate_uai
from aio_proxy.parsers.tranche_effectif import validate_tranche_effectif_salarie


def extract_text_parameters(
    request,
) -> Tuple[Dict[str, Union[str, None, bool]], int, int]:
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
    page = parse_and_validate_page(request)
    per_page = parse_and_validate_per_page(request)
    terms = parse_and_validate_terms(request)
    activite_principale = validate_activite_principale(
        clean_parameter(request, param="activite_principale")
    )
    code_postal = validate_code_postal(clean_parameter(request, param="code_postal"))
    departement = validate_departement(clean_parameter(request, param="departement"))
    is_entrepreneur_individuel = validate_is_entrepreneur_individuel(
        clean_parameter(request, param="is_entrepreneur_individuel")
    )
    section_activite_principale = validate_section_activite_principale(
        clean_parameter(request, param="section_activite_principale")
    )
    tranche_effectif_salarie = validate_tranche_effectif_salarie(
        clean_parameter(request, param="tranche_effectif_salarie")
    )
    nom_dirigeant = parse_parameter(request, param="nom_dirigeant")
    prenoms_dirigeant = parse_parameter(request, param="prenoms_dirigeant")
    min_date_naiss_dirigeant = parse_and_validate_date(
        request, param="date_naissance_dirigeant_min"
    )
    max_date_naiss_dirigeant = parse_and_validate_date(
        request, param="date_naissance_dirigeant_max"
    )
    is_finess = validate_is_field(request, param="is_finess")
    is_uai = validate_is_field(request, param="is_uai")
    is_colter = validate_is_field(request, param="is_colter")
    is_entrepreneur_spectacle = validate_is_field(request, param="is_entrepreneur_spectacle")
    is_rge = validate_is_field(request, param="is_rge")
    idcc = validate_idcc(clean_parameter(request, param="idcc"))
    finess = validate_finess(clean_parameter(request, param="finess"))
    uai = validate_uai(clean_parameter(request, param="uai"))
    colter_code_insee = validate_colter_code_insee(clean_parameter(request, param="colter_code_insee"))
    nom_elu = parse_parameter(request, param="nom_elu")
    prenoms_elu = parse_parameter(request, param="prenoms_elu")

    validate_date_range(min_date_naiss_dirigeant, max_date_naiss_dirigeant)

    parameters = {
        "terms": terms,
        "activite_principale_unite_legale": activite_principale,
        "code_postal": code_postal,
        "departement": departement,
        "is_entrepreneur_individuel": is_entrepreneur_individuel,
        "section_activite_principale": section_activite_principale,
        "tranche_effectif_salarie_unite_legale": tranche_effectif_salarie,
        "nom_dirigeant": nom_dirigeant,
        "prenoms_dirigeant": prenoms_dirigeant,
        "min_date_naiss_dirigeant": min_date_naiss_dirigeant,
        "max_date_naiss_dirigeant": max_date_naiss_dirigeant,
        "is_uai": is_uai,
        "is_finess": is_finess,
        "is_colter": is_colter,
        "is_entrepreneur_spectacle": is_entrepreneur_spectacle,
        "is_rge": is_rge,
        "idcc": idcc,
        "finess": finess,
        "uai": uai,
        "colter_code_insee": colter_code_insee,
        "nom_elu": nom_elu,
        "prenoms_elu": prenoms_elu,
    }

    # Check if at least one param has been provided in the request
    # It is easier to do it by checking if the param dict has only None values rather
    # than parse the request to check
    check_empty_params(parameters)

    check_no_param_and_length_terms(parameters)

    return parameters, page, per_page


def extract_geo_parameters(request):
    page = parse_and_validate_page(request)
    per_page = parse_and_validate_per_page(request)
    lat = parse_and_validate_latitude(request)
    lon = parse_and_validate_longitude(request)
    radius = parse_and_validate_radius(request)
    activite_principale = validate_activite_principale(
        clean_parameter(request, param="activite_principale")
    )
    section_activite_principale = validate_section_activite_principale(
        clean_parameter(request, param="section_activite_principale")
    )
    parameters = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "activite_principale_unite_legale": activite_principale,
        "section_activite_principale": section_activite_principale,
    }
    return parameters, page, per_page
