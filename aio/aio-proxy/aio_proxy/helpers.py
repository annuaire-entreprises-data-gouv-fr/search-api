import json


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return json.dumps(message)


def hide_fields(search_result: list) -> list:
    """Hide concatenation fields in search results."""
    hidden_fields = {
        "concat_nom_adr_siren",
        "concat_enseigne_adresse",
        "liste_adresse",
        "liste_enseigne",
    }
    unite_legale = [
        {field: value for field, value in unite.items() if field not in hidden_fields}
        for unite in search_result
    ]
    return unite_legale
