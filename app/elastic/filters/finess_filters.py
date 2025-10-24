from elasticsearch_dsl import Q


def build_id_finess_filter(id_finess, with_inner_hits=False, matching_size=10):
    finess_geo = Q(
        "nested",
        path="unite_legale.etablissements",
        query=Q(
            "match",
            unite_legale__etablissements__liste_finess={
                "query": id_finess,
                "_name": "Filter id:liste_finess",
            },
        ),
    )

    if with_inner_hits:
        finess_geo = Q(
            "nested",
            path="unite_legale.etablissements",
            query=Q(
                "match",
                unite_legale__etablissements__liste_finess={
                    "query": id_finess,
                    "_name": "Filter id:liste_finess",
                },
            ),
            inner_hits={
                "size": matching_size,
                "sort": {
                    "unite_legale.etablissements.etat_administratif": {"order": "asc"}
                },
            },
        )

    finess_jur = Q(
        "match",
        unite_legale__liste_finess_juridique={
            "query": id_finess,
            "_name": "Filter id:liste_finess_juridique",
        },
    )

    return Q("bool", should=[finess_geo, finess_jur], minimum_should_match=1)
