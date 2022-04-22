import json


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string"""
    message = {"message": text}
    return json.dumps(message)
