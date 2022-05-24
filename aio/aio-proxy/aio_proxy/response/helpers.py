import json


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return json.dumps(message)


def set_default_to_none(dict, key):
    """Set value to value of key if key found in dict, otherwise set value to None."""
    value = dict[key] if key in dict else None
    return value
