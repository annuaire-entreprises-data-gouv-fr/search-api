from aio_proxy.labels.helpers import valid_fields


def select_fields_to_include(
    include_fields, etablissements, score, slug, response: dict
):
    # Remove the fields from the result
    for field in valid_fields:
        if field not in include_fields and field.lower() in response:
            del response[field.lower()]

    # etablissements, score and slug are special fields used only by annuaire and a few
    # special users. These fields are always hidden, unless explicitly selected
    special_fields = {"ETABLISSEMENTS": etablissements, "SLUG": slug, "SCORE": score}
    for field in special_fields:
        if field in include_fields:
            response[field.lower()] = special_fields[field]

    return response
