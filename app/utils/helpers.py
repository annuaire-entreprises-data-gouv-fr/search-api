import ast
import logging
from datetime import datetime
from hashlib import sha256

import requests
from dotenv import load_dotenv

from app.config import settings

load_dotenv()


def fetch_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_content = response.json()
        return json_content
    except requests.RequestException as e:
        # Handle exceptions (e.g., network issues, invalid JSON, etc.)
        raise RuntimeError(f"Error fetching JSON from {url}: {str(e)}")


def convert_to_year_month(date_string):
    try:
        date_object = datetime.strptime(date_string, "%d/%m/%Y")
        formatted_date = date_object.strftime("%Y-%m")
        return formatted_date
    except ValueError:
        logging.warning(f"Invalid date of birth for `élus` : {date_string}")
        return None


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


def is_dev_env():
    return settings.env == "dev"


def serialize_error_text(text: str):
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return message


def get_value(data_dict, key, default=None):
    """
    Get the value associated with the given key from the dictionary.
    """
    if not data_dict:
        return default
    return data_dict.get(key, default)


def hash_string(string: str):
    hashed_string = sha256(string.encode("utf-8")).hexdigest()
    return hashed_string


def create_fields_to_include(search_params):
    if search_params.minimal:
        if search_params.include is None:
            return []
        else:
            return search_params.include
    else:
        return [
            "SIEGE",
            "FINANCES",
            "COMPLEMENTS",
            "DIRIGEANTS",
            "MATCHING_ETABLISSEMENTS",
        ]


def create_admin_fields_to_include(search_params):
    if search_params.include_admin is None:
        return []
    else:
        return search_params.include_admin


def evaluate_field(field_value):
    """
    Attempts to evaluate a field value using literal_eval from the ast module.

    Parameters:
        field_value (str): The value of the field to be evaluated.

    Returns:
        The evaluated value if successful, otherwise None.
    """
    if field_value is not None:
        try:
            return ast.literal_eval(field_value)
        except ValueError:
            return None
    else:
        return None


def string_list_to_string(string_list):
    if string_list is None:
        return None
    elif string_list.strip("[]") == "nan":
        return None
    else:
        elements = string_list.strip("[]").split(", ")
        # Remove surrounding quotes from each element
        cleaned_elements = [element.strip("'") for element in elements]
        # Join the elements into a single string
        return ", ".join(cleaned_elements)


def convert_date_to_iso(date_str):
    """
    Convert a datetime string to a date string in ISO format (YYYY-MM-DD).

    Parameters:
    date_str (str): The datetime string to convert.

    Returns:
    str: The date string in ISO format or None if the input format is incorrect.
    """
    if date_str is None:
        return None
    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.date().isoformat()
    except ValueError:
        # Handle incorrect date format
        return None
