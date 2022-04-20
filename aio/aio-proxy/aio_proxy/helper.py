import json


def serialize(text: str) -> object:
    message = {"message": text}
    return json.dumps(message)
