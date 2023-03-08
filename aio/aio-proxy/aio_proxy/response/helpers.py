import json
import os
from hashlib import sha256

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


def format_nom_complet(
    nom_complet,
    sigle=None,
    denomination_usuelle_1=None,
    denomination_usuelle_2=None,
    denomination_usuelle_3=None,
):
    """Add `denomination usuelle` fields and `sigle` to `nom_complet`."""
    all_denomination_usuelle = ""
    for item in [
        denomination_usuelle_1,
        denomination_usuelle_2,
        denomination_usuelle_3,
    ]:
        if item:
            all_denomination_usuelle += f"{item} "
    if all_denomination_usuelle:
        nom_complet = f"{nom_complet} ({all_denomination_usuelle.strip()})"
    if sigle:
        nom_complet = f"{nom_complet} ({sigle})"
    if nom_complet:
        return nom_complet.upper()
    # if nom_complet is null
    return None


def hash_string(string: str):
    hashed_string = sha256(string.encode("utf-8")).hexdigest()
    return hashed_string
