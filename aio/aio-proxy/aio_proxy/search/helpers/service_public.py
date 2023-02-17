from aio_proxy.labels.helpers import (
    natures_juridiques,
    natures_juridiques_service_public,
)


def build_list_natures_juridiques(est_service_public=None):
    """Create liste of `natures juridiques` corresponding to the `est_service_public`
    filter value.

    If `est_service_public` is True, return `natures juridiques` list corresponding
    to a `service public` (list which was self defined without official reference).

    If `est_service_public` is False, return `natures juridiques` list that is not a
    `service public`.
    """
    if est_service_public is None:
        return None
    if est_service_public:
        liste_natures_juridiques = [
            nature_juridique for nature_juridique in natures_juridiques_service_public
        ]
    else:
        liste_natures_juridiques = [
            nature_juridique
            for nature_juridique in natures_juridiques
            if nature_juridique not in natures_juridiques_service_public
        ]
    return liste_natures_juridiques
