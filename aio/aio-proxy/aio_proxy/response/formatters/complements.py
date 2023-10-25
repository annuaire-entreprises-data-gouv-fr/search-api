from aio_proxy.response.formatters.collectivite_territoriale import (
    format_collectivite_territoriale,
)
from aio_proxy.response.formatters.insee_bool import format_insee_bool
from aio_proxy.response.unite_legale_model import Complements


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
    egapro_renseignee = get_field("egapro_renseignee")
    est_association = get_field("est_association")
    est_bio = get_field("est_bio")
    est_entrepreneur_individuel = get_field(
        "est_entrepreneur_individuel", default=False
    )
    est_entrepreneur_spectacle = get_field("est_entrepreneur_spectacle")
    est_ess = format_insee_bool(get_field("economie_sociale_solidaire_unite_legale"))
    est_finess = get_field("est_finess")
    est_organisme_formation = get_field("est_organisme_formation")
    est_qualiopi = get_field("est_qualiopi")
    liste_id_organisme_formation = get_field("liste_id_organisme_formation")
    est_rge = get_field("est_rge")
    est_service_public = get_field("est_service_public")
    est_societe_mission = format_insee_bool(get_field("est_societe_mission"))
    est_uai = get_field("est_uai")
    identifiant_association = get_field("identifiant_association_unite_legale")
    statut_entrepreneur_spectacle = get_field(
        "statut_entrepreneur_spectacle",
    )
    return Complements(
        collectivite_territoriale=collectivite_territoriale,
        convention_collective_renseignee=convention_collective_renseignee,
        egapro_renseignee=egapro_renseignee,
        est_association=est_association,
        est_bio=est_bio,
        est_entrepreneur_individuel=est_entrepreneur_individuel,
        est_entrepreneur_spectacle=est_entrepreneur_spectacle,
        est_ess=est_ess,
        est_finess=est_finess,
        est_organisme_formation=est_organisme_formation,
        est_qualiopi=est_qualiopi,
        liste_id_organisme_formation=liste_id_organisme_formation,
        est_rge=est_rge,
        est_service_public=est_service_public,
        est_societe_mission=est_societe_mission,
        est_uai=est_uai,
        identifiant_association=identifiant_association,
        statut_entrepreneur_spectacle=statut_entrepreneur_spectacle,
    )
