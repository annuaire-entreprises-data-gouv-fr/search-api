# app/elastic/helpers/health.py
import logging

from elasticsearch.dsl import connections


def is_elasticsearch_available() -> bool:
    """Returns True if Elasticsearch is reachable, False otherwise."""
    try:
        es_client = connections.get_connection()
        return es_client.ping()
    except Exception as error:
        logging.error(f"Elasticsearch healthcheck failed: {error}")
        return False
