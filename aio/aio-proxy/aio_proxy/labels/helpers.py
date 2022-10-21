import json

labels_file_path = "aio_proxy/labels/"


def load_file(file_name: str):
    with open(f"{labels_file_path}{file_name}") as json_file:
        file_decoded = json.load(json_file)
    return file_decoded


codes_communes = load_file("codes-communes.json")
codes_naf = load_file("codes-NAF.json")
tranches_effectifs = load_file("tranches-effectifs.json")
sections_codes_naf = load_file("sections-codes-NAF.json")
