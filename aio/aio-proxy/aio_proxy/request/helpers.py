def match_bool_to_insee_value(bool_value: bool) -> str | None:
    """Match bool filter value to corresponding INSEE field value .

    Args:
        bool_value (str): `est_var` value extracted from request

    Returns:
        None if `est_var`is None.
        "O" if `est_var` is True.
        "N" if `est_var` is False.

    """
    if bool_value is None:
        return None
    if bool_value is True:
        insee_value = "O"
    else:
        insee_value = "N"
    return insee_value


def str_to_list(string_values: str) -> list[str]:
    values_list = string_values.split(",")
    return values_list


def clean_str(param: str):
    param = param.replace("-", " ")
    param_clean = param.replace(" ", "").upper()
    return param_clean


def check_params_are_none_except_excluded(fields_dict, excluded_fields):
    for key, value in fields_dict.items():
        if key not in excluded_fields and value is not None:
            return False
    return True
