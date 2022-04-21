import json

labels_file_path = "aio_proxy/labels/"


def load_file(file_name: str):
    with open(f"{labels_file_path}{file_name}") as json_file:
        file_decoded = json.load(json_file)
    return file_decoded


def get_codes_naf():
    return load_file("codes-NAF.json")


def get_tranches_effectifs():
    return load_file("tranches-effectifs.json")
