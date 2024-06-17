import json

labels_file_path = "aio_proxy/labels/"


def load_file(file_name: str):
    with open(f"{labels_file_path}{file_name}") as json_file:
        file_decoded = json.load(json_file)
    return file_decoded


CODES_NAF = load_file("codes-NAF.json")
DEPARTEMENTS = load_file("departements.json")
NATURES_JURIDIQUES = load_file("natures-juridiques.json")
TRANCHES_EFFECTIFS = load_file("tranches-effectifs.json")
REGIONS = load_file("regions.json")
SECTIONS_CODES_NAF = load_file("sections-codes-NAF.json")
NATURES_ENTREPRISES = load_file("natures-entreprises.json")
