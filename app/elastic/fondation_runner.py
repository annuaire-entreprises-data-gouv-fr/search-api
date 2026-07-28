import logging
from datetime import timedelta

from elasticsearch.dsl import Q

from app.elastic.es_index import StructureMapping
from app.elastic.filters.fondation import filter_by_numero_rnf, filter_fondations
from app.elastic.helpers.helpers import (
    execute_and_agg_total_results_by_identifiant,
    page_through_results,
)
from app.elastic.parsers.numero_rnf import is_numero_rnf
from app.elastic.queries.fondation import FONDATION_PATH, build_fondation_text_query
from app.utils.cache import cache_strategy


class FondationRunner:
    MIN_EXECUTION_TIME = 400
    MAX_TOTAL_RESULTS = 10000
    # The response is built from the fondation alone so there is no need to fetch unite_legale
    SOURCE_FIELDS = ["identifiant", FONDATION_PATH]

    def __init__(self, search_params):
        self.search_params = search_params
        self.es_search_client = StructureMapping.search()
        self.es_search_results = None
        self.total_results = None
        self.execution_time = None
        self.run()

    def build_es_search_query(self):
        search = self.es_search_client.source(includes=self.SOURCE_FIELDS)
        search = filter_fondations(search)

        query_terms = self.search_params.terms
        # Filter by `numéro RNF` first (if the query is a `numéro RNF`), and return
        # the fondation directly without text search.
        if is_numero_rnf(query_terms):
            search = filter_by_numero_rnf(search, query_terms.strip())
        else:
            search = search.query(Q(build_fondation_text_query(query_terms)))

        # Collapse is used to aggregate the results by identifiant. It is the
        # consequence of separating large documents into smaller ones.
        search = search.update_from_dict({"collapse": {"field": "identifiant"}})

        # Fondations are sorted on relevance alone.
        search = search.extra(track_scores=True).sort({"_score": {"order": "desc"}})

        self.es_search_client = search

    def execute_and_format_es_search(self):
        self.es_search_client = page_through_results(self)
        es_response = self.es_search_client.execute()
        self.total_results = es_response.hits.total.value
        self.execution_time = es_response.took
        logging.info(f"Elasticsearch execution time: {self.execution_time}")

        # Due to performance issues when aggregating on filter queries, we use
        # aggregation on total_results only when total_results is lower than
        # 10 000 results. If total_results is higher than 10 000 results,
        # the aggregation causes timeouts on API. We return by default 10 000 results.
        if self.total_results < self.MAX_TOTAL_RESULTS:
            execute_and_agg_total_results_by_identifiant(self)

        self.es_search_results = [
            {
                "fondation": matching_structure.to_dict()[FONDATION_PATH],
                "meta": matching_structure.meta.to_dict(),
            }
            for matching_structure in es_response.hits
        ]

    def should_cache_for_how_long(self):
        """Determines how long to cache search results based on conditions:
        - 24 hours if execution time > MIN_EXECUTION_TIME
        - 30 minutes if searching by Numéro RNF
        - No caching (0 minutes) otherwise or on error"""
        if self.execution_time and self.execution_time > self.MIN_EXECUTION_TIME:
            return timedelta(hours=24)
        if is_numero_rnf(self.search_params.terms):
            return timedelta(minutes=30)
        return timedelta(minutes=0)

    def run(self):
        self.build_es_search_query()

        def get_es_search_response():
            self.execute_and_format_es_search()
            return {
                "total_results": self.total_results,
                "response": self.es_search_results,
                "execution_time": self.execution_time,
            }

        # To make sure the page and page size are part of the cache key
        cache_key = page_through_results(self)

        cached_search_results = cache_strategy(
            cache_key,
            get_es_search_response,
            self.should_cache_for_how_long,
        )

        self.total_results = min(
            cached_search_results["total_results"], self.MAX_TOTAL_RESULTS
        )
        self.es_search_results = cached_search_results["response"]
        self.execution_time = cached_search_results["execution_time"]
