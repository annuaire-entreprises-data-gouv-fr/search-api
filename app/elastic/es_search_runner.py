import logging
from datetime import timedelta

from app.elastic.es_index import StructureMapping
from app.elastic.geo_search import build_es_search_geo_query
from app.elastic.helpers.helpers import (
    execute_and_agg_total_results_by_identifiant,
    extract_ul_and_etab_from_es_response,
    page_through_results,
)
from app.elastic.parsers.siren import is_siren
from app.elastic.parsers.siret import is_siret
from app.elastic.text_search import build_es_search_text_query
from app.service.search_type import SearchType
from app.utils.cache import cache_strategy
from app.utils.helpers import is_dev_env

MIN_EXECUTION_TIME = 400
MAX_TOTAL_RESULTS = 10000


class ElasticSearchRunner:
    def __init__(self, search_params=None, search_type=None):
        self.es_search_client = StructureMapping.search()
        self.es_index = StructureMapping.Index.name
        self.search_type = search_type
        self.search_params = search_params
        self.has_full_text_query = False
        self.es_search_results = None
        self.total_results = None
        self.execution_time = None
        if search_type:
            self.run()

    def sort_es_search_query(self):
        # Sorting is very heavy on performance if there are no
        # search terms (only filters). As there is no search terms, we can
        # exclude this sorting because score is the same for all results
        # documents. Beware, nom and prenoms are search fields.
        if self.has_full_text_query:
            self.es_search_client = self.es_search_client.sort(
                {"_score": {"order": "desc"}},
                {"unite_legale.etat_administratif_unite_legale": {"order": "asc"}},
                {"unite_legale.nombre_etablissements_ouverts": {"order": "desc"}},
            )
        # If only filters are used, use nombre établissements ouverts to sort the
        # results
        else:
            self.es_search_client = self.es_search_client.sort(
                {"unite_legale.nombre_etablissements_ouverts": {"order": "desc"}},
            )

    def execute_and_format_es_search(self):
        self.es_search_client = page_through_results(self)
        es_response = self.es_search_client.execute()
        self.total_results = es_response.hits.total.value
        self.execution_time = es_response.took

        # Due to performance issues when aggregating on filter queries, we use
        # aggregation on total_results only when total_results is lower than
        # 10 000 results. If total_results is higher than 10 000 results,
        # the aggregation causes timeouts on API. We return by default 10 000 results.
        max_results_exceeded = self.total_results >= MAX_TOTAL_RESULTS
        if not max_results_exceeded:
            execute_and_agg_total_results_by_identifiant(self)

        self.es_search_results = []
        for matching_structure in es_response.hits:
            matching_structure_dict = extract_ul_and_etab_from_es_response(
                matching_structure
            )
            self.es_search_results.append(matching_structure_dict)

    def sort_and_execute_es_search_query(self):
        self.es_search_client = self.es_search_client.extra(track_scores=True)

        # explain query result in dev env
        if is_dev_env():
            self.es_search_client = self.es_search_client.extra(
                track_scores=True, explain=True
            )

        # Collapse is used to aggregate the results by siren. It is the consequence
        # of separating large documents into smaller ones
        self.es_search_client = self.es_search_client.update_from_dict(
            {"collapse": {"field": "identifiant"}}
        )

        # Sort results
        self.sort_es_search_query()

        # Execute search, only called if key not found in cache
        # (see cache strategy below)
        def get_es_search_response():
            self.execute_and_format_es_search()
            es_results_to_cache = {
                "total_results": self.total_results,
                "response": self.es_search_results,
                "execution_time": self.execution_time,
            }
            return es_results_to_cache

        # To make sure the page and page size are part of the cache key
        cache_key = page_through_results(self)

        cached_search_results = cache_strategy(
            cache_key,
            get_es_search_response,
            self.should_cache_for_how_long,
        )

        self.total_results = cached_search_results["total_results"]
        self.es_search_results = cached_search_results["response"]
        self.execution_time = cached_search_results["execution_time"]

    def should_cache_for_how_long(self):
        """Determines how long to cache search results based on conditions:
        - 24 hours if execution time > MIN_EXECUTION_TIME
        - 30 minutes if searching by SIREN/SIRET
        - No caching (0 minutes) otherwise or on error"""
        try:
            query_terms = self.search_params.terms
            if self.execution_time > MIN_EXECUTION_TIME:
                return timedelta(hours=24)
            if is_siren(query_terms) or is_siret(query_terms):
                return timedelta(minutes=30)
            return timedelta(minutes=0)  # Default case when no conditions are met
        except KeyError as error:
            logging.info(f"Error getting search execution time: {error}")
            return timedelta(minutes=0)

    def run(self):
        if self.search_type == SearchType.TEXT:
            build_es_search_text_query(self)
        elif self.search_type == SearchType.GEO:
            build_es_search_geo_query(self)
        self.sort_and_execute_es_search_query()
