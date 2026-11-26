from app.service.formatters.dirigeants import format_dirigeants
from app.service.formatters.non_diffusible import NON_DIFFUSIBLE_MASK, mask_unite_legale

GERANT = {
    "nom": "DUPONT",
    "prenoms": "JEAN",
    "date_de_naissance": "1970-01",
    "role": "Gérant",
    "nationalite": "Française",
}

PRESIDENT_PM = {
    "siren": "000000000",
    "denomination": "SOCIETE EXEMPLE",
    "role": "Président de SAS",
}


def test_dirigeant_pp_demissionnaire_exposes_date_demission():
    [dirigeant] = format_dirigeants(
        dirigeants_pp=[{**GERANT, "date_demission": "2026-07-31"}]
    )
    assert dirigeant.date_demission == "2026-07-31"


def test_dirigeant_pm_demissionnaire_exposes_date_demission():
    [dirigeant] = format_dirigeants(
        dirigeants_pm=[{**PRESIDENT_PM, "date_demission": "2026-04-30"}]
    )
    assert dirigeant.date_demission == "2026-04-30"


def test_dirigeant_without_date_demission_has_none():
    dirigeants = format_dirigeants(dirigeants_pp=[GERANT], dirigeants_pm=[PRESIDENT_PM])
    assert [d.date_demission for d in dirigeants] == [None, None]


def test_same_person_demissionnaire_and_in_office_stays_two_entries():
    dirigeants = format_dirigeants(
        dirigeants_pp=[{**GERANT, "date_demission": "2026-07-31"}, GERANT]
    )
    assert [(d.qualite, d.date_demission) for d in dirigeants] == [
        ("Gérant", "2026-07-31"),
        ("Gérant", None),
    ]


def test_non_diffusible_ul_keeps_date_demission_of_dirigeant_pp():
    dirigeants = format_dirigeants(
        dirigeants_pp=[{**GERANT, "date_demission": "2026-07-31"}]
    )
    formatted_ul = {"dirigeants": [d.dict(exclude_unset=True) for d in dirigeants]}
    [dirigeant] = mask_unite_legale(formatted_ul, is_pm=True, is_ul_nd=True)[
        "dirigeants"
    ]
    assert dirigeant["nom"] == NON_DIFFUSIBLE_MASK
    assert dirigeant["date_demission"] == "2026-07-31"
