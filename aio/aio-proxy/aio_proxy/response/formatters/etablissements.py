from aio_proxy.response.helpers import get_value


def format_etablissement(source_etablissement):
    formatted_etablissement = {
        "activite_principale": get_value(source_etablissement, "activite_principale"),
        "activite_principale_registre_metier": get_value(
            source_etablissement, "activite_principale_registre_metier"
        ),
        "cedex": get_value(source_etablissement, "cedex"),
        "code_pays_etranger": get_value(source_etablissement, "code_pays_etranger"),
        "code_postal": get_value(source_etablissement, "code_postal"),
        "commune": get_value(source_etablissement, "commune"),
        "complement_adresse": get_value(source_etablissement, "complement_adresse"),
        "date_creation": get_value(source_etablissement, "date_creation"),
        "date_debut_activite": get_value(source_etablissement, "date_debut_activite"),
        "distribution_speciale": get_value(
            source_etablissement, "distribution_speciale"
        ),
        "enseigne_1": get_value(source_etablissement, "enseigne_1"),
        "enseigne_2": get_value(source_etablissement, "enseigne_2"),
        "enseigne_3": get_value(source_etablissement, "enseigne_3"),
        "est_source_etablissement": get_value(
            source_etablissement, "est_source_etablissement"
        ),
        "etat_administratif": get_value(source_etablissement, "etat_administratif"),
        "geo_adresse": get_value(source_etablissement, "geo_adresse"),
        "geo_id": get_value(source_etablissement, "geo_id"),
        "indice_repetition": get_value(source_etablissement, "indice_repetition"),
        "latitude": get_value(source_etablissement, "latitude"),
        "libelle_cedex": get_value(source_etablissement, "libelle_cedex"),
        "libelle_commune": get_value(source_etablissement, "libelle_commune"),
        "libelle_commune_etranger": get_value(
            source_etablissement, "libelle_commune_etranger"
        ),
        "libelle_pays_etranger": get_value(
            source_etablissement, "libelle_pays_etranger"
        ),
        "libelle_voie": get_value(source_etablissement, "libelle_voie"),
        "liste_finess": get_value(source_etablissement, "liste_finess"),
        "liste_idcc": get_value(source_etablissement, "liste_idcc"),
        "liste_rge": get_value(source_etablissement, "liste_rge"),
        "liste_uai": get_value(source_etablissement, "liste_uai"),
        "longitude": get_value(source_etablissement, "longitude"),
        "nom_commercial": get_value(source_etablissement, "nom_commercial"),
        "numero_voie": get_value(source_etablissement, "numero_voie"),
        "siret": get_value(source_etablissement, "siret"),
        "tranche_effectif_salarie": get_value(
            source_etablissement, "tranche_effectif_salarie"
        ),
        "type_voie": get_value(source_etablissement, "type_voie"),
        "adresse": get_value(source_etablissement, "adresse"),
        "coordonnees": get_value(source_etablissement, "coordonnees"),
        "departement": get_value(source_etablissement, "departement"),
    }
    return formatted_etablissement


def format_etablissements_list(etablissements=None):
    etablissements_formatted = []
    if etablissements:
        for etablissement in etablissements:
            etablissement_formatted = format_etablissement(etablissement)
            etablissements_formatted.append(etablissement_formatted)
    return etablissements_formatted


def format_siege(siege=None):
    siege_formatted = format_etablissement(siege)
    return siege_formatted
