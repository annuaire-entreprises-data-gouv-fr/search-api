import json

labels_file_path = "aio_proxy/labels/"


def load_file(file_name: str):
    with open(f"{labels_file_path}{file_name}") as json_file:
        file_decoded = json.load(json_file)
    return file_decoded


codes_naf = load_file("codes-NAF.json")
departements = load_file("departements.json")
natures_juridiques = load_file("natures-juridiques.json")
tranches_effectifs = load_file("tranches-effectifs.json")
regions = load_file("regions.json")
sections_codes_naf = load_file("sections-codes-NAF.json")
valid_fields_to_select = [
    "COMPLEMENTS",
    "DIRIGEANTS",
    "FINANCES",
    "SIEGE",
    "MATCHING_ETABLISSEMENTS",
]
valid_admin_fields_to_select = ["ETABLISSEMENTS", "SCORE", "SLUG"]
