import ast
import json
import os
from hashlib import sha256

from dotenv import load_dotenv

load_dotenv()

APM_URL = os.getenv("APM_URL")

CURRENT_ENV = os.getenv("ENV")


def is_dev_env():
    return CURRENT_ENV == "dev"


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return json.dumps(message)


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
    if string_list.strip("[]") == "nan" or string_list is None:
        return None
    else:
        elements = string_list.strip("[]").split(", ")
        # Remove surrounding quotes from each element
        cleaned_elements = [element.strip("'") for element in elements]
        # Join the elements into a single string
        return ", ".join(cleaned_elements)
