from aio_proxy.decorators.value_exception import value_exception_handler
from aio_proxy.labels.helpers import (
    valid_admin_fields_to_select,
    valid_fields_to_select,
)


def validate_selected_fields(list_fields_clean: list[str], admin=False):
    if admin:
        valid_fields_to_check = valid_admin_fields_to_select
    else:
        valid_fields_to_check = valid_fields_to_select
    if list_fields_clean is None:
        return None
    for field in list_fields_clean:
        if field not in valid_fields_to_check:
            valid_fields_lowercase = [field.lower() for field in valid_fields_to_check]
            raise ValueError(
                f"Au moins un champ à inclure est non valide. "
                f"Les champs valides : {valid_fields_lowercase}."
            )
    return list_fields_clean


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
