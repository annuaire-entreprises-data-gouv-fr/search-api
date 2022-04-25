import re
from typing import Dict, Optional, Tuple, Union

from aio_proxy.labels.helpers import codes_naf, tranches_effectifs


def parse_page_parameters(request) -> Tuple[int, int]:
    try:
        page = int(request.rel_url.query.get("page", 1)) - 1  # default 1
        per_page = int(request.rel_url.query.get("per_page", 10))  # default 10
    except (TypeError, ValueError) as error:
        raise ValueError(str(error))
    return page, per_page


def parse_and_clean_parameter(request, param: str, default_value=None):
    """Extract and clean param from request.
    Remove white spaces and use upper case.

    Args:
        request: HTTP request
        param (str): parameter to extract from request
        default_value:

    Returns:
        None if None.
        clean_param otherwise.

    """
    param = request.rel_url.query.get(param, default_value)
    if param is None:
        return None
    param_clean = param.replace(" ", "").upper()
    return param_clean


def validate_code_postal(code_postal_clean: str) -> Optional[str]:
    """Check the validity of code_postal.

    Args:
        code_postal_clean(str, optional): code postal extracted and cleaned.

    Returns:
        None if code_postal_clean is None.
        code_postal_clean if valid.

    Raises:
        ValueError: if code_postal_clean not valid.
    """
    if code_postal_clean is None:
        return None
    if len(code_postal_clean) != 5:
        raise ValueError("Code postal doit contenir 5 caractères !")
    codes_valides = "^((0[1-9])|([1-8][0-9])|(9[0-8])|(2A)|(2B))[0-9]{3}$"
    if not re.search(codes_valides, code_postal_clean):
        raise ValueError("Code postal non valide.")
    return code_postal_clean


def validate_activite_principale(activite_principale_clean: str) -> Optional[str]:
    """Check the validity of activite_principale.

    Args:
        activite_principale_clean(str, optional): activite_principale extracted and
                                                cleaned.

    Returns:
        None if activite_principale_clean is None.
        activite_principale_clean if valid.

    Raises:
        ValueError: if activite_principale_clean not valid.
    """
    if activite_principale_clean is None:
        return None
    if len(activite_principale_clean) != 6:
        raise ValueError("Activité principale doit contenir 6 caractères.")
    if activite_principale_clean not in codes_naf:
        raise ValueError("Activité principale inconnue.")
    return activite_principale_clean


def validate_is_entrepreneur_individuel(
    is_entrepreneur_individuel_clean: str,
) -> Optional[bool]:
    """Check the validity of is_entrepreneur_individuel.

    Args:
        is_entrepreneur_individuel_clean(str, optional): is_entrepreneur_individuel
                                                        extracted and cleaned.

    Returns:
        None if is_entrepreneur_individuel_clean is None.
        True if is_entrepreneur_individuel_clean==YES.
        False if is_entrepreneur_individuel_clean==NO.

    Raises:
        ValueError: otherwise.
    """
    if is_entrepreneur_individuel_clean is None:
        return None
    if is_entrepreneur_individuel_clean not in ["YES", "NO"]:
        raise ValueError(
            "Seuls les valeurs 'yes' ou bien 'no' sont possibles pour 'is_"
            "entrepreneur_individuel'."
        )
    return is_entrepreneur_individuel_clean == "YES"


def validate_tranche_effectif_salarie_entreprise(
    tranche_effectif_salarie_entreprise_clean: str,
) -> Optional[str]:
    """Check the validity of tranche_effectif_salarie_entreprise.

    Args:
        tranche_effectif_salarie_entreprise_clean(str, optional):
         tranche_effectif_salarie_entreprise extracted and cleaned.

    Returns:
        None if tranche_effectif_salarie_entreprise_clean is None.
        tranche_effectif_salarie_entreprise_clean if valid.

    Raises:
        ValueError: if tranche_effectif_salarie_entreprise_clean not valid.
    """
    if tranche_effectif_salarie_entreprise_clean is None:
        return None
    if len(tranche_effectif_salarie_entreprise_clean) != 2:
        raise ValueError("Tranche salariés doit contenir 2 caractères.")
    if tranche_effectif_salarie_entreprise_clean not in tranches_effectifs:
        raise ValueError("Tranche salariés non valide.")
    return tranche_effectif_salarie_entreprise_clean


def parse_and_validate_terms(request) -> str:
    """Extract search terms from request.

    Args:
        request: HTTP request.

    Returns:
        terms if given.
    Raises:
        ValueError: otherwise.
    """
    try:
        terms = request.rel_url.query["q"]
        return terms
    except KeyError:
        raise ValueError(
            "Veuillez indiquer la requête avec le paramètre: ?q=ma+recherche."
        )


def parse_and_validate_latitude(request):
    try:
        lat = float(request.rel_url.query.get("lat"))
        if lat > 90 or lat < -90:
            raise ValueError
        return lat
    except (TypeError, KeyError, ValueError):
        raise ValueError("Veuillez indiquer une latitude entre -90° et 90°.")


def parse_and_validate_longitude(request):
    try:
        lon = float(request.rel_url.query.get("long"))
        if lon > 180 or lon < -180:
            raise ValueError
        return lon
    except (TypeError, KeyError, ValueError):
        raise ValueError("Veuillez indiquer une longitude entre -180° et 180°.")


def parse_and_validate_radius(request):
    try:
        radius = float(request.rel_url.query.get("radius", 5))  # default 5
        return radius
    except (TypeError, ValueError):
        raise ValueError("Veuillez indiquer un radius entier ou flottant, en km.")


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
    page, per_page = parse_page_parameters(request)
    terms = parse_and_validate_terms(request)
    activite_principale = validate_activite_principale(
        parse_and_clean_parameter(request, param="activite_principale")
    )
    code_postal = validate_code_postal(
        parse_and_clean_parameter(request, param="code_postal")
    )
    is_entrepreneur_individuel = validate_is_entrepreneur_individuel(
        parse_and_clean_parameter(request, param="is_entrepreneur_individuel")
    )
    tranche_effectif_salarie_entreprise = validate_tranche_effectif_salarie_entreprise(
        parse_and_clean_parameter(request, param="tranche_effectif_salarie_entreprise")
    )
    parameters = {
        "terms": terms,
        "activite_principale_entreprise": activite_principale,
        "code_postal": code_postal,
        "is_entrepreneur_individuel": is_entrepreneur_individuel,
        "tranche_effectif_salarie_entreprise": tranche_effectif_salarie_entreprise,
    }

    return parameters, page, per_page


def extract_geo_parameters(request):
    page, per_page = parse_page_parameters(request)
    lat = parse_and_validate_latitude(request)
    lon = parse_and_validate_longitude(request)
    radius = parse_and_validate_radius(request)
    activite_principale = validate_activite_principale(
        parse_and_clean_parameter(request, param="activite_principale")
    )
    parameters = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "activite_principale_entreprise": activite_principale,
    }
    return parameters, page, per_page
