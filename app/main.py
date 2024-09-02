import logging

import yaml
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from elasticsearch_dsl import connections
from fastapi import FastAPI

from app.config import (
    APM_CONFIG,
    CURRENT_ENV,
    ELASTIC_PASSWORD,
    ELASTIC_URL,
    ELASTIC_USER,
    OPEN_API_PATH,
)
from app.logging import setup_logging, setup_sentry
from app.router import router

# Setup logging
setup_logging()

# Connect to Elasticsearch
connections.create_connection(
    hosts=[ELASTIC_URL],
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    retry_on_timeout=True,
)

app = FastAPI(
    title="API Recherche d'entreprises",
    version="1.0.0",
    docs_url=None,
    redoc_url="/docs/",
)


# Load OpenAPI YAML file
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    logging.info(f"+++++++++++{OPEN_API_PATH}")
    with open(OPEN_API_PATH) as file:
        openapi_schema = yaml.safe_load(file)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Sentry Integration and Elastic APM Integration for Production
if CURRENT_ENV == "prod":
    apm_client = make_apm_client(APM_CONFIG)
    app.add_middleware(ElasticAPM, client=apm_client)
    setup_sentry()

# Include the router
app.include_router(router)
