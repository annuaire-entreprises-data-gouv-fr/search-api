import importlib.resources as pkg_resources
import json

import app.labels as labels_package

# List of module names to import
file_modules = [
    "codes-NAF",
    "departements",
    "natures-juridiques",
    "tranches-effectifs",
    "regions",
    "sections-codes-NAF",
    "natures-entreprises",
]


# Function to load JSON content from a module
def load_json_from_module(module_name: str):
    json_content = pkg_resources.read_text(labels_package, f"{module_name}.json")
    return json.loads(json_content)


# Load all JSON files into a dictionary
loaded_files = {
    module_name.upper(): load_json_from_module(module_name)
    for module_name in file_modules
}

# Accessing the data
CODES_NAF = loaded_files["CODES-NAF"]
DEPARTEMENTS = loaded_files["DEPARTEMENTS"]
NATURES_JURIDIQUES = loaded_files["NATURES-JURIDIQUES"]
TRANCHES_EFFECTIFS = loaded_files["TRANCHES-EFFECTIFS"]
REGIONS = loaded_files["REGIONS"]
SECTIONS_CODES_NAF = loaded_files["SECTIONS-CODES-NAF"]
NATURES_ENTREPRISES = loaded_files["NATURES-ENTREPRISES"]
