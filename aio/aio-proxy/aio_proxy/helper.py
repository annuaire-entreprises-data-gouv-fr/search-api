import json


def serialize(text: str) -> str:
    message = {"message": text}
    return json.dumps(message)
