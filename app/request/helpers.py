def match_bool_to_insee_value(bool_value: bool) -> str:
    """Match bool filter value to corresponding INSEE field value .

    Args:
        bool_value (str): `bool_value` value extracted from request

    Returns:
        "O" if `bool_value` is True.
        "N" if `bool_value` is False.

    """
    return "O" if bool_value else "N"


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
