import json
import os

from dotenv import load_dotenv

load_dotenv()

APM_URL = os.getenv("APM_URL")

CURRENT_ENV = os.getenv("ENV")

COLOR_URL = os.getenv("COLOR_URL")


def is_dev_env():
    return CURRENT_ENV == "dev"


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return json.dumps(message)


def get_value(dict, key, default=None):
    """Set value to value of key if key found in dict, otherwise set value to
    default."""
    value = dict[key] if key in dict else default
    return value
