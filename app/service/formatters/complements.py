from app.models.unite_legale import Complements
from app.service.formatters.collectivite_territoriale import (
    format_collectivite_territoriale,
)
from app.service.formatters.insee_bool import format_insee_bool
from app.utils.helpers import string_list_to_string


def format_complements(result_unite_legale):
    def get_field(field, default=None):
        return result_unite_legale.get(field, default)

    collectivite_territoriale = format_collectivite_territoriale(
        get_field("colter_code"),
        get_field("colter_code_insee"),
        get_field("colter_elus"),
        get_field("colter_niveau"),
    )
    convention_collective_renseignee = get_field("convention_collective_renseignee")
    liste_idcc = get_field("liste_idcc_unite_legale")
    egapro_renseignee = get_field("egapro_renseignee")
    est_achats_responsables = get_field("est_achats_responsables")
    est_alim_confiance = get_field("est_alim_confiance")
    est_association = get_field("est_association")
    est_bio = get_field("est_bio")
    est_entrepreneur_individuel = get_field(
        "est_entrepreneur_individuel", default=False
    )
    est_entrepreneur_spectacle = get_field("est_entrepreneur_spectacle")
    est_ess = get_field("est_ess")
    est_finess = get_field("est_finess")
    est_organisme_formation = get_field("est_organisme_formation")
    est_patrimoine_vivant = get_field("est_patrimoine_vivant")
    est_qualiopi = get_field("est_qualiopi")
    liste_id_organisme_formation = get_field("liste_id_organisme_formation")
    est_rge = get_field("est_rge")
    est_service_public = get_field("est_service_public")
    est_l100_3 = get_field("est_l100_3")
    est_siae = get_field("est_siae")
    est_societe_mission = format_insee_bool(get_field("est_societe_mission"))
    est_uai = get_field("est_uai")
    identifiant_association = get_field("identifiant_association_unite_legale")
    statut_entrepreneur_spectacle = get_field(
        "statut_entrepreneur_spectacle",
    )
    type_siae = string_list_to_string(get_field("type_siae"))
    return Complements(
        collectivite_territoriale=collectivite_territoriale,
        convention_collective_renseignee=convention_collective_renseignee,
        liste_idcc=liste_idcc,
        egapro_renseignee=egapro_renseignee,
        est_achats_responsables=est_achats_responsables,
        est_alim_confiance=est_alim_confiance,
        est_association=est_association,
        est_bio=est_bio,
        est_entrepreneur_individuel=est_entrepreneur_individuel,
        est_entrepreneur_spectacle=est_entrepreneur_spectacle,
        est_ess=est_ess,
        est_finess=est_finess,
        est_organisme_formation=est_organisme_formation,
        est_patrimoine_vivant=est_patrimoine_vivant,
        est_qualiopi=est_qualiopi,
        liste_id_organisme_formation=liste_id_organisme_formation,
        est_rge=est_rge,
        est_siae=est_siae,
        est_service_public=est_service_public,
        est_l100_3=est_l100_3,
        est_societe_mission=est_societe_mission,
        est_uai=est_uai,
        identifiant_association=identifiant_association,
        statut_entrepreneur_spectacle=statut_entrepreneur_spectacle,
        type_siae=type_siae,
    )
