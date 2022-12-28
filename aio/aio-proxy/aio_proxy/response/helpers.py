import json


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return json.dumps(message)


def get_value(dict, key, default=None):
    """Set value to value of key if key found in dict, otherwise set value to
    default."""
    value = dict[key] if key in dict else default
    return value


def format_collectivite_territoriale(
    colter_code=None, colter_code_insee=None, colter_elus=None, colter_niveau=None
):
    if colter_code is None:
        return None
    else:
        return {
            "code": colter_code,
            "code_insee": colter_code_insee,
            "elus": format_elus(colter_elus),
            "niveau": colter_niveau,
        }


def format_dirigeants(dirigeants_pp=None, dirigeants_pm=None):
    dirigeants = []
    if dirigeants_pp:
        for dirigeant_pp in dirigeants_pp:
            annee_de_naissance = (
                get_value(dirigeant_pp, "date_naissance")[:4]
                if get_value(dirigeant_pp, "date_naissance")
                else None
            )

            dirigeant = {
                "nom": get_value(dirigeant_pp, "nom"),
                "prenoms": get_value(dirigeant_pp, "prenoms"),
                "annee_de_naissance": annee_de_naissance,
                "qualite": get_value(dirigeant_pp, "qualite"),
                "type_dirigeant": "personne physique",
            }
            dirigeants.append(dirigeant)
    if dirigeants_pm:
        for dirigeant_pm in dirigeants_pm:
            sigle = (
                get_value(dirigeant_pm, "sigle")
                if get_value(dirigeant_pm, "sigle") != ""
                else None
            )
            dirigeant = {
                "siren": get_value(dirigeant_pm, "siren"),
                "denomination": get_value(dirigeant_pm, "denomination"),
                "sigle": sigle,
                "qualite": get_value(dirigeant_pm, "qualite"),
                "type_dirigeant": "personne morale",
            }
            dirigeants.append(dirigeant)
    return dirigeants


def format_elus(elus=None):
    format_elus = []
    if elus:
        for elu in elus:
            annee_de_naissance = (
                get_value(elu, "date_naissance")[:4]
                if get_value(elu, "date_naissance")
                else None
            )

            format_elu = {
                "nom": get_value(elu, "nom"),
                "prenoms": get_value(elu, "prenom"),
                "annee_de_naissance": annee_de_naissance,
                "fonction": get_value(elu, "fonction"),
                "sexe": get_value(elu, "sexe"),
            }
            format_elus.append(format_elu)
    return format_elus


def format_etablissements(etablissements=None):
    etablissements_formatted = []
    if etablissements:
        for etablissement in etablissements:
            etablissement = {
                "activite_principale": get_value(etablissement, "activite_principale"),
                "activite_principale_registre_metier": get_value(etablissement, "activite_principale_registre_metier"),
                "cedex": get_value(etablissement, "cedex"),
                "code_pays_etranger": get_value(etablissement, "code_pays_etranger"),
                "code_postal": get_value(etablissement, "code_postal"),
                "commune": get_value(etablissement, "commune"),
                "complement_adresse": get_value(etablissement, "complement_adresse"),
                "date_creation": get_value(etablissement, "date_creation"),
                "date_debut_activite": get_value(etablissement, "date_debut_activite"),
                "distribution_speciale": get_value(etablissement, "distribution_speciale"),
                "enseigne_1": get_value(etablissement, "enseigne_1"),
                "enseigne_2": get_value(etablissement, "enseigne_2"),
                "enseigne_3": get_value(etablissement, "enseigne_3"),
                "est_siege": get_value(etablissement, "est_siege"),
                "etat_administratif": get_value(etablissement, "etat_administratif"),
                "geo_adresse": get_value(etablissement, "geo_adresse"),
                "geo_id": get_value(etablissement, "geo_id"),
                "indice_repetition": get_value(etablissement, "indice_repetition"),
                "latitude": get_value(etablissement, "latitude"),
                "libelle_cedex": get_value(etablissement, "libelle_cedex"),
                "libelle_commune": get_value(etablissement, "libelle_commune"),
                "libelle_commune_etranger": get_value(etablissement, "libelle_commune_etranger"),
                "libelle_pays_etranger": get_value(etablissement, "libelle_pays_etranger"),
                "libelle_voie": get_value(etablissement, "libelle_voie"),
                "liste_finess": get_value(etablissement, "liste_finess"),
                "liste_idcc": get_value(etablissement, "liste_idcc"),
                "liste_rge": get_value(etablissement, "liste_rge"),
                "liste_uai": get_value(etablissement, "liste_uai"),
                "longitude": get_value(etablissement, "longitude"),
                "nom_commercial": get_value(etablissement, "nom_commercial"),
                "numero_voie": get_value(etablissement, "numero_voie"),
                "siret": get_value(etablissement, "siret"),
                "tranche_effectif_salarie": get_value(etablissement, "tranche_effectif_salarie"),
                "type_voie": get_value(etablissement, "type_voie"),
                "adresse": get_value(etablissement, "adresse"),
                "coordonnees": get_value(etablissement, "coordonnees"),
                "departement": get_value(etablissement, "departement"),
            }
            etablissements_formatted.append(etablissement)
    return etablissements_formatted


def format_matched_etablissements():
    return matched_etablissements


def format_bool_field(value):
    if value is None:
        return False
    else:
        return True


def format_ess(value):
    if value is None or value == "N":
        return False
    else:
        return True
