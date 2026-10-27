import pytest

from app.elastic.filters.diffusion import (
    build_non_diffusible_query,
    build_protege_query,
)
from app.service.siren_protege import siren_protege_list


@pytest.fixture(autouse=True)
def empty_siren_protege_list():
    siren_protege_list.set_sirens(frozenset())
    yield
    siren_protege_list.set_sirens(frozenset())


def test_protege_query_with_empty_list_only_checks_index_flag():
    assert build_protege_query().to_dict() == {
        "bool": {
            "should": [{"term": {"unite_legale.est_protege": True}}],
            "minimum_should_match": 1,
        }
    }


def test_protege_query_includes_in_memory_sirens_sorted():
    siren_protege_list.set_sirens(frozenset({"200000000", "100000000"}))

    assert build_protege_query().to_dict()["bool"]["should"] == [
        {"term": {"unite_legale.est_protege": True}},
        {"terms": {"unite_legale.siren": ["100000000", "200000000"]}},
    ]


def test_protege_query_excludes_sirens_already_flagged_in_index():
    siren_protege_list.set_sirens(
        frozenset({"200000000", "100000000"}),
        sirens_flagged_in_index=frozenset({"100000000"}),
    )

    assert build_protege_query().to_dict()["bool"]["should"] == [
        {"term": {"unite_legale.est_protege": True}},
        {"terms": {"unite_legale.siren": ["200000000"]}},
    ]


def test_non_diffusible_query_matches_statut_p_or_protege():
    assert build_non_diffusible_query().to_dict()["bool"]["should"] == [
        {"term": {"unite_legale.statut_diffusion_unite_legale": "P"}},
        build_protege_query().to_dict(),
    ]
