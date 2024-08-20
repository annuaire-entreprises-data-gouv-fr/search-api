import logging
import os

import yaml
from dotenv import load_dotenv
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from elasticsearch_dsl import connections
from fastapi import FastAPI

from app.response.helpers import APM_URL, CURRENT_ENV
from app.router import router

load_dotenv()

# Get env variables
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_URL = os.getenv("ELASTIC_URL")
DSN_SENTRY = os.getenv("DSN_SENTRY")

load_dotenv()

open_api_path = "doc/open-api.yml"

logging.basicConfig(level=logging.INFO)

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
    with open(open_api_path) as file:
        openapi_schema = yaml.safe_load(file)
    app.openapi_schema = openapi_schema
    return app.openapi_schemab


# Assign the custom OpenAPI method to the FastAPI app
app.openapi = custom_openapi

# Elastic APM Integration
if CURRENT_ENV != "dev":
    apm_config = {
        "SERVICE_NAME": "SEARCH APM",
        "SERVER_URL": APM_URL,
        "ENVIRONMENT": CURRENT_ENV,
    }
    apm_client = make_apm_client(apm_config)
    app.add_middleware(ElasticAPM, client=apm_client)


# Include the router
app.include_router(router)
