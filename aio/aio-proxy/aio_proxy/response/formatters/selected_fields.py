from aio_proxy.labels.helpers import valid_fields


def select_fields_to_include(
    include_fields, etablissements, score, slug, response: dict
):
    # Create a list of fields to remove from the result
    fields_to_remove = [
        field
        for field in response
        if field.upper() not in include_fields and field.upper() in valid_fields
    ]

    # Remove the fields from the result
    for field in fields_to_remove:
        del response[field]

    # etablissements, score and slug are special fields used only by annuaire and a few
    # special users. These fields are always hidden, unless explicitly selected
    special_fields = {"ETABLISSEMENTS": etablissements, "SLUG": slug, "SCORE": score}
    for field in special_fields:
        if field in include_fields:
            response[field.lower()] = special_fields[field]

    return response
