import os

import yaml
from dotenv import load_dotenv
from elasticsearch_dsl import connections
from fastapi import FastAPI

from app.router import router

load_dotenv()

# Get env variables
ENV = os.getenv("ENV")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_URL = os.getenv("ELASTIC_URL")
DSN_SENTRY = os.getenv("DSN_SENTRY")

load_dotenv()

ENV = os.getenv("ENV")
open_api_path = "doc/open-api.yml"

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
    return app.openapi_schema


# Assign the custom OpenAPI method to the FastAPI app
app.openapi = custom_openapi


# Include the router
app.include_router(router)
