from aio_proxy.decorators.value_exception import value_exception_handler


def should_include_etablissements(admin_fields):
    if admin_fields and "ETABLISSEMENTS" in admin_fields:
        return True
    return None


@value_exception_handler(
    error="Veuillez indiquer si vous souhaitez une réponse minimale avec le filtre"
    " 'minimal=True' avant de préciser les champs à inclure."
)
def validate_inclusion_fields(minimal: bool, include_fields: list[str]):
    if include_fields and minimal is None or (include_fields and minimal is False):
        raise ValueError


def check_if_lon_and_lat_exist(params):
    if "lat" not in params:
        raise ValueError("Veuillez indiquer une latitude entre -90° et 90°.")
    if "lon" not in params:
        raise ValueError("Veuillez indiquer une longitude entre -180° et 180°.")
