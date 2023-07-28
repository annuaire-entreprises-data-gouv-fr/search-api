from aio_proxy.labels.helpers import valid_admin_fields, valid_fields


def validate_selected_fields(list_fields_clean: list[str], admin=False):
    if admin:
        valid_fields_to_check = valid_admin_fields
    else:
        valid_fields_to_check = valid_fields
    if list_fields_clean is None:
        return None
    for field in list_fields_clean:
        if field not in valid_fields_to_check:
            raise ValueError(
                f"Au moins un champ est non valide. "
                f"Les champs valides : {valid_fields_to_check}."
            )
    return list_fields_clean


def include_etablissements(admin_fields):
    if admin_fields and "ETABLISSEMENTS" in admin_fields:
        return True
    return False
